# Salesforce

System of action for GTM Expansion Intelligence (fictional FieldPilot).

## Status

| Area | Status |
|------|--------|
| FieldPilot Account model (Type, ParentId, custom/repurposed fields, synthetic seed) | **Implemented** (documented; org-backed) |
| Contacts (seed data in org) | **Implemented** |
| Product2 + `External_Product_Code__c` | **Implemented** (catalog model; Product2 seed rows planned next) |
| `Product_Entitlement__c` entitlement model | **Implemented** (object/fields; entitlement seed rows planned next) |
| SFDX metadata under `force-app/` | **Not yet retrieved** into this repo |
| Product2 / entitlement seed data loads | **Planned** |
| `Account_Signal__c`, `AI_Recommendation__c` | **Planned** |
| Apex / LWC / Flow / API sync clients | **Planned** |
| Quote / Order / Contract / Asset / full RLM | **Deferred** — not required for current MVP |

Authoritative Account, Product, and entitlement field list: [docs/project-context.md](../docs/project-context.md).

## Role

- Hold customer/location hierarchy and commercial context.
- Hold Product2 catalog and `Product_Entitlement__c` (current entitlement / product-adoption source).
- Receive actionable intelligence (signals + AI recommendations) later.
- Support human review.
- Create parent-level Expansion Opportunities only after seller acceptance of Customer-scoped recommendations.

Do **not** store high-volume raw product telemetry or support history here — that belongs in Snowflake.

Salesforce remains authoritative for current entitlement state. Snowflake may later hold an analytical `entitlement_snapshot` copy.

## Account hierarchy (implemented)

| Scope | Modeling |
|-------|----------|
| Business | `Account.Type = Business`; `Customer_Id__c`; `NumberofLocations__c`; primarily `Customer_ARR__c` |
| Location | `Account.Type = Location`; `Account.ParentId` → Business; `Location_Id__c`; `Revenue_Weight__c`; `Location_Status__c` |

Record type: `Field_Pilot` (`012g7000004KDoPAAW`).

Superseded planned names (do not recreate): `Account_Scope__c`, `Branch_Count__c`, `Customer_Segment__c`, `Service_Vertical__c`.

## Product catalog and entitlements (implemented)

| Object | Role |
|--------|------|
| Product2 | Product catalog |
| Product2.`External_Product_Code__c` | Cross-system product key (Text(50), External ID) |
| `Product_Entitlement__c` | Lightweight entitlement / adoption context for MVP |

Entitlements may attach to **Business** or **Location** Accounts via `Account__c`. Do not assume parent entitlement enables every child location.

Full field definitions: [docs/project-context.md](../docs/project-context.md). Salesforce summary: [docs/data-model.md](docs/data-model.md).

**Deferred:** Asset / Contract as entitlement source; Quote / Order / full Revenue Cloud lifecycle.

## Planned / deferred objects (beyond current foundation)

| Object | Status |
|--------|--------|
| Opportunity (+ AI linkage fields) | Planned (expansion action after human approval) |
| `Account_Signal__c` | Planned |
| `AI_Recommendation__c` | Planned |
| Quote, Order, Contract, Asset | Deferred (RLM / full commercial lifecycle) |

## Layout

| Path | Purpose |
|------|---------|
| `force-app/main/default/` | Future SFDX metadata |
| `docs/data-model.md` | Salesforce Account + Product / entitlement + planned object notes |
| `docs/metadata-strategy.md` | How metadata will be retrieved and governed |

See also:

- [docs/project-context.md](../docs/project-context.md)
- [docs/data-model.md](../docs/data-model.md)
- [docs/human-in-the-loop.md](../docs/human-in-the-loop.md)
- [docs/design-decisions.md](../docs/design-decisions.md)
