from datetime import datetime, timedelta
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.db.models import Alert, SensorReading


def create_reading(db: Session, reading: SensorReading) -> SensorReading:
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


def create_alert(db: Session, alert: Alert) -> Alert:
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_metrics(db: Session, lookback_hours: int) -> dict:
    total_messages = db.scalar(select(func.count()).select_from(SensorReading)) or 0
    lookback_start = datetime.utcnow() - timedelta(hours=lookback_hours)
    recent_alerts = (
        db.scalar(
            select(func.count())
            .select_from(Alert)
            .where(Alert.timestamp >= lookback_start)
        )
        or 0
    )
    return {"total_messages": total_messages, "recent_alerts": recent_alerts}


def get_alerts(db: Session, limit: int, offset: int) -> list[Alert]:
    return (
        db.query(Alert)
        .order_by(Alert.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_readings(
    db: Session,
    limit: int,
    offset: int,
    topic: str | None,
    start: datetime | None,
    end: datetime | None,
) -> list[SensorReading]:
    query = db.query(SensorReading)
    if topic:
        query = query.filter(SensorReading.topic == topic)
    if start:
        query = query.filter(SensorReading.timestamp >= start)
    if end:
        query = query.filter(SensorReading.timestamp <= end)
    return (
        query.order_by(SensorReading.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_latest_per_topic(db: Session) -> list[SensorReading]:
    subquery = (
        db.query(
            SensorReading.topic,
            func.max(SensorReading.timestamp).label("max_ts"),
        )
        .group_by(SensorReading.topic)
        .subquery()
    )
    return (
        db.query(SensorReading)
        .join(
            subquery,
            (SensorReading.topic == subquery.c.topic)
            & (SensorReading.timestamp == subquery.c.max_ts),
        )
        .order_by(SensorReading.topic.asc())
        .all()
    )
