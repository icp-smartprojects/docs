## Learning Engine Runbook

### Env vars
- `DB_URL` (default `sqlite:///./learning_engine.db`)
- `CORS_ORIGINS` (comma-separated, default `*`)
- `METRICS_ENABLED` (default `true`)

### Run locally
```bash
cd learning-engine
uvicorn app:app --reload --port 52004
```

### DB init / migrations
- Schema is created automatically on startup via SQLAlchemy metadata.
- For Postgres, set `DB_URL=postgresql+psycopg2://user:pass@host:5432/db`.

### Seed sample data
```bash
cd learning-engine
python scripts/seed_learning_engine.py
```

### Smoke test
```bash
curl -X POST http://localhost:52004/api/v1/learning/events \
  -H "content-type: application/json" \
  -d '{"events":[{"event_type":"OUTCOME_SIGNAL","payload":{"decision_id":"smoke","decision_type":"BUY","predicted_confidence":0.6,"actual_outcome":"win","timeframe":"M5"}}]}'
curl http://localhost:52004/api/v1/learning/state
```

### Observability
- Liveness: `GET /healthz`
- Readiness: `GET /readyz`
- Metrics: `GET /metrics` (Prometheus format)

### Troubleshooting
- Slow responses: check DB_URL (SQLite on network shares can be slow); move to Postgres.
- Missing events: verify JSON schema (422 errors) and logs.
- Policy stuck: ensure `/api/v1/learning/events` receives OUTCOME_SIGNAL to drive calibration.
