from datetime import datetime
from pydantic import BaseModel


class SensorReadingOut(BaseModel):
    id: int
    topic: str
    timestamp: datetime
    temperature: float | None
    humidity: float | None
    voltage: float | None
    current: float | None
    pressure: float | None
    raw_payload: str

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    topic: str
    timestamp: datetime
    violated_keys: str
    actual_values: str

    class Config:
        from_attributes = True


class MetricsOut(BaseModel):
    total_messages: int
    recent_alerts: int
