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

## Deployment (Render)

This repository includes a `render.yaml` manifest so you can deploy both services on Render.

Steps:

1. Push your code to GitHub (already done).
2. Sign in to Render and create a new service from GitHub. Select the repository.
3. Render will detect services from `render.yaml`:
   - `sensor-monitor-backend` (Docker service) — it builds from `backend/Dockerfile`.
   - `sensor-monitor-frontend` (Static site) — it runs `cd frontend && npm ci && npm run build` and publishes `frontend/dist`.
4. In Render dashboard, set environment variables for the backend (Database connection, MQTT broker credentials). Example env vars:
   - `SQLALCHEMY_DATABASE_URI` (e.g. `mysql+pymysql://user:pass@<HOST>:3306/sensordb`)
   - `MQTT_BROKER_HOST`, `MQTT_BROKER_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD`
5. For the database, you can provision a managed MySQL instance in Render or use an external managed DB and set the connection string.

Notes:
- The repo also contains a GitHub Actions workflow to build and publish the frontend to `gh-pages` on every push to `main` (.github/workflows/deploy-frontend.yml). If you prefer Render to host the frontend, you can disable that workflow.
- If you prefer another provider (Fly.io, Railway, VPS), I can add specific deployment scripts or workflows.

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
