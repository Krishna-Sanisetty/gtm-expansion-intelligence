# Salesforce metadata strategy

## Principles

1. **Docs first.** The implemented FieldPilot Account, Product2, and `Product_Entitlement__c` models are documented in [docs/project-context.md](../../docs/project-context.md). Metadata retrieval must match that model — not early scaffold field names or deferred RLM objects.
2. **Prefer standard fields.** Use `Account.Type`, `Account.ParentId`, `NumberofLocations__c`, and Product2 before inventing custom equivalents.
3. **Source-control metadata** under `salesforce/force-app/` once retrieved; never commit org credentials, session tokens, or auth files.
4. **No telemetry in CRM.** Product usage and support history stay in Snowflake. Salesforce holds hierarchy, Product2, `Product_Entitlement__c`, and (later) synced signals / recommendations.
5. **Separate Implemented vs Planned vs Deferred.**
   - **Implemented:** Account model, Contacts, Product2 + `External_Product_Code__c`, `Product_Entitlement__c`
   - **Planned:** Product/entitlement seed loads, signals, AI recommendations, Apex/LWC/Flow, Opportunity AI fields
   - **Deferred:** full Revenue Cloud / RLM (Quote → Order → Contract → Asset)

## Superseded planned API names

Do not recreate these in metadata:

| Do not create | Use instead |
|---------------|-------------|
| `Account_Scope__c` | `Account.Type` |
| `Branch_Count__c` | `NumberofLocations__c` |
| `Customer_Segment__c` | `Segment__c` |
| `Service_Vertical__c` | `Service_Verticals__c` |

Do not introduce a second custom entitlement object that duplicates `Product_Entitlement__c` without a documented architecture decision.

Do not add Asset / Contract / Quote / Order dependencies for current entitlement unless explicitly requested.

## Retrieval expectations (when authorized)

When pulling metadata from the FieldPilot org:

- Record type `Field_Pilot`
- Custom fields listed in `docs/project-context.md` (Account + Product2 + `Product_Entitlement__c`)
- Picklist / multipicklist value sets for Type, Segment, Service_Verticals, Customer_Status, Location_Status, Entitlement_Status
- Layouts only if needed for demo; prefer thin retrieval over full org dumps

Until metadata is in `force-app/`, treat the documentation as the contract for seeds, Snowflake joins, and agent work.

## Related ADRs

See [docs/design-decisions.md](../../docs/design-decisions.md) ADRs 13–20.
