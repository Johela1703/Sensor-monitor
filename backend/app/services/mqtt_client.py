import json
import logging
from typing import Any
import paho.mqtt.client as mqtt
from app.core.config import get_settings
from app.db.crud import create_alert, create_reading
from app.db.models import Alert, SensorReading
from app.db.session import SessionLocal

logger = logging.getLogger("mqtt")

EXPECTED_KEYS = ["temperature", "humidity", "voltage", "current", "pressure"]


def _parse_payload(payload: bytes) -> dict[str, Any] | None:
    try:
        return json.loads(payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        logger.warning("Invalid JSON payload")
        return None


def _extract_values(data: dict[str, Any]) -> dict[str, float | None]:
    values: dict[str, float | None] = {}
    for key in EXPECTED_KEYS:
        if key in data:
            try:
                values[key] = float(data[key])
            except (TypeError, ValueError):
                values[key] = None
        else:
            values[key] = None
    return values


def _evaluate_thresholds(values: dict[str, float | None], thresholds: dict) -> tuple[list[str], dict]:
    violated = []
    actual_values: dict[str, float] = {}
    for key, value in values.items():
        if value is None:
            continue
        limits = thresholds.get(key, {})
        min_val = limits.get("min")
        max_val = limits.get("max")
        if min_val is not None and value < min_val:
            violated.append(key)
            actual_values[key] = value
        if max_val is not None and value > max_val:
            violated.append(key)
            actual_values[key] = value
    return violated, actual_values


class MqttListener:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.client = mqtt.Client()
        if settings.mqtt_username:
            self.client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def start(self) -> None:
        logger.info("Connecting to MQTT broker at %s:%s", self.settings.mqtt_broker_host, self.settings.mqtt_broker_port)
        self.client.connect(self.settings.mqtt_broker_host, self.settings.mqtt_broker_port, 60)
        self.client.loop_start()

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: dict, rc: int) -> None:
        if rc == 0:
            logger.info("Connected to MQTT broker")
            for topic in self.settings.topics_list:
                client.subscribe(topic)
                logger.info("Subscribed to %s", topic)
        else:
            logger.error("MQTT connection failed with code %s", rc)

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        payload = _parse_payload(msg.payload)
        if payload is None:
            return

        values = _extract_values(payload)
        db = SessionLocal()
        try:
            reading = SensorReading(
                topic=msg.topic,
                temperature=values.get("temperature"),
                humidity=values.get("humidity"),
                voltage=values.get("voltage"),
                current=values.get("current"),
                pressure=values.get("pressure"),
                raw_payload=json.dumps(payload),
            )
            create_reading(db, reading)

            violated, actual_values = _evaluate_thresholds(values, self.settings.thresholds)
            if violated:
                alert = Alert(
                    topic=msg.topic,
                    violated_keys=",".join(violated),
                    actual_values=json.dumps(actual_values),
                )
                create_alert(db, alert)
                logger.warning("Alert triggered on %s: %s", msg.topic, violated)
        finally:
            db.close()
