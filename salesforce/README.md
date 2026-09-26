# Salesforce

System of action for GTM Expansion Intelligence (fictional FieldPilot).

## Status

| Area | Status |
|------|--------|
| FieldPilot Account model (Type, ParentId, custom/repurposed fields, synthetic seed) | **Implemented** (documented; org-backed) |
| SFDX metadata under `force-app/` | **Not yet retrieved** into this repo |
| Contacts, Products, Assets, Contracts | **Planned** |
| `Account_Signal__c`, `AI_Recommendation__c` | **Planned** |
| Apex / LWC / Flow / API sync clients | **Planned** |

Authoritative Account field list: [docs/project-context.md](../docs/project-context.md).

## Role

- Hold customer/location hierarchy and commercial context.
- Receive actionable intelligence (signals + AI recommendations) later.
- Support human review.
- Create parent-level Expansion Opportunities only after seller acceptance of Customer-scoped recommendations.

Do **not** store high-volume raw product telemetry or support history here — that belongs in Snowflake.

## Account hierarchy (implemented)

| Scope | Modeling |
|-------|----------|
| Business | `Account.Type = Business`; `Customer_Id__c`; `NumberofLocations__c`; primarily `Customer_ARR__c` |
| Location | `Account.Type = Location`; `Account.ParentId` → Business; `Location_Id__c`; `Revenue_Weight__c`; `Location_Status__c` |

Record type: `Field_Pilot` (`012g7000004KDoPAAW`).

Superseded planned names (do not recreate): `Account_Scope__c`, `Branch_Count__c`, `Customer_Segment__c`, `Service_Vertical__c`.

## Planned objects (beyond Account)

Standard: Contact, Product2, Asset, Contract, Opportunity, Quote, Order.

Custom (planned): `Account_Signal__c`, `AI_Recommendation__c`.

## Layout

| Path | Purpose |
|------|---------|
| `force-app/main/default/` | Future SFDX metadata |
| `docs/data-model.md` | Salesforce Account + planned object notes |
| `docs/metadata-strategy.md` | How metadata will be retrieved and governed |

See also:

- [docs/project-context.md](../docs/project-context.md)
- [docs/data-model.md](../docs/data-model.md)
- [docs/human-in-the-loop.md](../docs/human-in-the-loop.md)
- [docs/design-decisions.md](../docs/design-decisions.md)
