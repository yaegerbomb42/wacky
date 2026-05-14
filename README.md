# Agent O

Production-oriented autonomous task system with single-active-task queue execution, autonomy modes, confirm/fix loop payloads, and self-improvement checkpoints.

## Stack
- FastAPI API server
- PostgreSQL persistence
- Redis for queue signaling
- RQ worker for single-task execution
- React frontend (Vite)
- Docker Compose deployment

## Quick start
```bash
docker compose up --build
```

Services:
- API: http://localhost:8000
- Web: http://localhost:5173
- PgAdmin optional omitted

## Security note
The platform enforces hard policy rails and does not support abusive identity, quota-evasion, or unauthorized financial behavior.
