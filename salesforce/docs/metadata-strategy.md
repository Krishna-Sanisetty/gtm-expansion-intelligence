# Salesforce metadata strategy

## Principles

1. **Docs first for Account.** The implemented FieldPilot Account model is documented in [docs/project-context.md](../../docs/project-context.md). Metadata retrieval must match that model — not the early scaffold field names.
2. **Prefer standard fields.** Use `Account.Type`, `Account.ParentId`, and `NumberofLocations__c` before inventing custom equivalents.
3. **Source-control metadata** under `salesforce/force-app/` once retrieved; never commit org credentials, session tokens, or auth files.
4. **No telemetry in CRM.** Product usage and support history stay in Snowflake. Salesforce holds hierarchy, commercial context, and (later) synced signals / recommendations.
5. **Separate Implemented vs Planned.** Account fields are Implemented. Signals, AI recommendations, Apex/LWC/Flow, and Revenue Cloud remain Planned until explicitly delivered.

## Superseded planned API names

Do not recreate these in metadata:

| Do not create | Use instead |
|---------------|-------------|
| `Account_Scope__c` | `Account.Type` |
| `Branch_Count__c` | `NumberofLocations__c` |
| `Customer_Segment__c` | `Segment__c` |
| `Service_Vertical__c` | `Service_Verticals__c` |

## Retrieval expectations (when authorized)

When pulling metadata from the FieldPilot org:

- Record type `Field_Pilot`
- Custom fields listed in `docs/project-context.md`
- Picklist / multipicklist value sets for Type, Segment, Service_Verticals, Customer_Status, Location_Status
- Layouts only if needed for demo; prefer thin retrieval over full org dumps

Until metadata is in `force-app/`, treat the documentation as the contract for seeds, Snowflake joins, and agent work.

## Related ADRs

See [docs/design-decisions.md](../../docs/design-decisions.md) ADRs 13–18.
