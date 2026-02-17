import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import get_settings
from app.db.session import Base, engine
from app.services.mqtt_client import MqttListener

logging.basicConfig(level=logging.INFO)

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")

mqtt_listener = MqttListener()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    mqtt_listener.start()
