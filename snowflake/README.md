# Snowflake

System of analysis for GTM Expansion Intelligence.

## Status

**Planned.** DDL, seed data, views, and pipelines are not implemented.
Directories are reserved for incremental work.

## Role

Store analytical copies of:

- customer / location hierarchy
- product telemetry
- support facts
- entitlement snapshots (planned source: Salesforce `Product_Entitlement__c` + Product2 — not Asset / Contract for the current MVP)
- recommendation outcomes
- pipeline / watermark state

High-volume historical telemetry does **not** belong in Salesforce.

Salesforce remains authoritative for commercial and entitlement state.

## Layout

| Path | Purpose |
|------|---------|
| `ddl/` | Table definitions |
| `seed/` | Synthetic seed scripts |
| `queries/` | Analysis / batch queries |
| `views/` | Analytical views |
| `pipelines/` | Load / transform jobs |

See [docs/data-model.md](../docs/data-model.md).
