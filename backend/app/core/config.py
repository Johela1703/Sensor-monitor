import json
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sensor Monitor API"
    app_env: str = "local"
    sqlalchemy_database_uri: str = "mysql+pymysql://app:app@localhost:3306/sensordb"

    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_username: str | None = None
    mqtt_password: str | None = None
    mqtt_topics: str = "sensor/temperature,sensor/humidity,sensor/voltage,sensor/current,sensor/pressure"

    thresholds_json: str = (
        "{\"temperature\":{\"min\":0,\"max\":60},"
        "\"humidity\":{\"min\":10,\"max\":90},"
        "\"voltage\":{\"min\":2.5,\"max\":4.2},"
        "\"current\":{\"min\":0,\"max\":2.0},"
        "\"pressure\":{\"min\":90,\"max\":110}}"
    )

    alert_lookback_hours: int = 24

    @property
    def topics_list(self) -> list[str]:
        return [topic.strip() for topic in self.mqtt_topics.split(",") if topic.strip()]

    @property
    def thresholds(self) -> dict:
        try:
            return json.loads(self.thresholds_json)
        except json.JSONDecodeError:
            return {}

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
