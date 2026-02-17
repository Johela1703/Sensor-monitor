# Full Stack Sensor Monitor

This project provides a FastAPI backend that ingests MQTT sensor data and a React frontend that visualizes readings and alerts.

## Architecture
- Backend: FastAPI + SQLAlchemy + MySQL + MQTT (paho-mqtt)
- Frontend: React (Vite) with a dashboard, alerts, and raw data views
- Infra: Docker Compose with MySQL and Mosquitto

## Backend setup
1. Create a virtual environment and install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Copy env file and update values:
   ```bash
   copy .env.example .env
   ```
3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Frontend setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run dev server:
   ```bash
   npm run dev
   ```

## Docker (backend + db + mqtt)
```bash
docker compose up --build
```

## Hosting notes (exploration)
- Backend: render, fly.io, railway, or any Docker host; ensure outbound MQTT and DB connectivity.
- Frontend: static build can be hosted on Vercel, Netlify, or any object storage with CDN.
- For production, use managed MySQL and a reliable MQTT broker (e.g., HiveMQ Cloud).

## MQTT payload format
Expected JSON keys:
```json
{
  "temperature": 22.5,
  "humidity": 55.2,
  "voltage": 3.3,
  "current": 0.12,
  "pressure": 101.2
}
```

## API endpoints
- `GET /api/health`
- `GET /api/metrics`
- `GET /api/sensors/latest`
- `GET /api/sensors/raw?topic=...&start=...&end=...&limit=...&offset=...`
- `GET /api/alerts?limit=...&offset=...`
