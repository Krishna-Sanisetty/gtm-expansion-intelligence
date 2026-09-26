# Salesforce

System of action for GTM Expansion Intelligence.

## Status

**Planned.** No Salesforce metadata, Apex, or API clients are implemented
in this foundation pass.

## Role

Receive actionable intelligence (signals + AI recommendations). Support
human review. Create parent-level Expansion Opportunities only after
seller acceptance of Customer-scoped recommendations.

## Planned objects

Standard: Account, Contact, Product2, Asset, Contract, Opportunity, Quote, Order.

Custom (planned): `Account_Signal__c`, `AI_Recommendation__c`.

## Layout

| Path | Purpose |
|------|---------|
| `force-app/main/default/` | Future SFDX metadata |
| `docs/` | Salesforce-specific design notes |

See [docs/data-model.md](../docs/data-model.md) and
[docs/human-in-the-loop.md](../docs/human-in-the-loop.md).
