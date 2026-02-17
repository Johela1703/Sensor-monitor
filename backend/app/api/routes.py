from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.crud import get_alerts, get_latest_per_topic, get_metrics, get_readings
from app.db.session import get_db
from app.schemas import AlertOut, MetricsOut, SensorReadingOut
from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/metrics", response_model=MetricsOut)
def metrics(db: Session = Depends(get_db)) -> MetricsOut:
    settings = get_settings()
    return MetricsOut(**get_metrics(db, settings.alert_lookback_hours))


@router.get("/sensors/latest", response_model=list[SensorReadingOut])
def latest(db: Session = Depends(get_db)) -> list[SensorReadingOut]:
    return get_latest_per_topic(db)


@router.get("/alerts", response_model=list[AlertOut])
def alerts(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> list[AlertOut]:
    return get_alerts(db, limit, offset)


@router.get("/sensors/raw", response_model=list[SensorReadingOut])
def raw_data(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    topic: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    db: Session = Depends(get_db),
) -> list[SensorReadingOut]:
    return get_readings(db, limit, offset, topic, start, end)
