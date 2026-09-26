# Backend

FastAPI service for GTM Expansion Intelligence.

## Status

**Skeleton only.** Implemented: `GET /health`.

## Planned

- Recommendation review / sync APIs
- Typed schemas for signals and recommendations
- Configuration via `pydantic-settings`
- Integration with batch orchestration and Salesforce sync helpers

## Local health check

```bash
uvicorn backend.app.main:app --reload --port 8741
curl http://127.0.0.1:8741/health
```

Expected:

```json
{"status":"ok","service":"gtm-expansion-intelligence"}
```
