# Azure

Future production-style runtime. Development is local-first.

## Status

**Planned.** No Azure-specific business logic and no infrastructure
templates are implemented yet.

## Preferred future services

- Azure Container Apps
- Azure Container Apps Jobs
- Azure OpenAI
- Azure AI Search
- Key Vault
- Azure Monitor / Application Insights

Same application code should be containerized and deployed — do not fork
local vs cloud business implementations.

## Layout

| Path | Purpose |
|------|---------|
| `container-apps/` | App service definitions |
| `jobs/` | Scheduled batch job definitions |
| `monitoring/` | Alerts / dashboards |
| `infrastructure/` | IaC (planned) |
