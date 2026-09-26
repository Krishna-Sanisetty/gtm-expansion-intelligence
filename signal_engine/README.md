# Signal Engine

Deterministic derivation of location- and customer-scoped signals from
verified operational facts.

## Status

**Documentation stub only.** `signals.py` describes the design. No rules
or fake thresholds are implemented.

## Principles

- Facts before AI
- The model cannot invent evidence
- Preserve location-level evidence before aggregating
- Product entitlement coverage is location-aware (source: Salesforce `Product_Entitlement__c`; Business or Location scope)

## Layout (planned)

| Path | Purpose |
|------|---------|
| `signals.py` | Signal generation design notes / future entrypoints |
| `models.py` | Typed signal schemas |
| `rules/` | Deterministic rule definitions |
| `aggregation/` | Hierarchy-aware customer aggregation |
| `tests/` | Unit tests against synthetic fixtures |

See also: [docs/signal-design.md](../docs/signal-design.md),
[docs/hierarchy-and-aggregation.md](../docs/hierarchy-and-aggregation.md).
