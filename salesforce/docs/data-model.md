# Salesforce data model (FieldPilot)

Primary source of truth for Account fields: [docs/project-context.md](../../docs/project-context.md).

This file summarizes the CRM-facing model for work under `salesforce/`.

---

## Implemented — Account hierarchy

```text
Business Account (Type = Business)
  └── Location Account (Type = Location, ParentId → Business)
```

| Rule | Detail |
|------|--------|
| Record type | `Field_Pilot` / Id `012g7000004KDoPAAW` |
| Scope discriminator | `Account.Type` ∈ {Business, Location, Other} — **not** `Account_Scope__c` |
| Hierarchy | `Account.ParentId` Location → Business |
| Opportunities | Business Account only |
| Synthetic volume | 10 Business + 50 Location |

### Business fields

| Field | Type / values | Notes |
|-------|---------------|-------|
| `Customer_Id__c` | Text(50), External ID | e.g. `FP-CUST-1001`; Business only |
| `Segment__c` | SMB \| Mid-Market \| Enterprise | replaces `Customer_Segment__c` |
| `Service_Verticals__c` | multi-select | HVAC; Plumbing; Roofing; Electrical; Fencing; Multi-Trade |
| `Platform_Go_Live_Date__c` | Date | tenure / lifecycle |
| `Customer_Status__c` | Prospect \| Onboarding \| Active \| At Risk \| Churned | expansion eligibility |
| `Technician_Count__c` | Number(8,0) | sum of locations in synthetic data |
| `Customer_ARR__c` | Currency(16,2) | primarily Business |
| `Customer_Health_Score__c` | Number(3,0) 0–100 | supporting context only |
| `NumberofLocations__c` | Number(3,0) | replaces `Branch_Count__c` |

### Location fields

| Field | Type / values | Notes |
|-------|---------------|-------|
| `Location_Id__c` | Text(50), External ID | e.g. `FP-LOC-2001`; Location only |
| `Segment__c` | SMB \| Mid-Market \| Enterprise | may mirror parent |
| `Service_Verticals__c` | multi-select | as above |
| `Technician_Count__c` | Number(8,0) | branch technicians |
| `Revenue_Weight__c` | Percent(5,2) | ~100% per Business; Location only |
| `Location_Status__c` | Active / Opening (synthetic) | non-active excluded from aggregation assumptions |
| `Customer_Health_Score__c` | Number(3,0) | supporting context |
| `Platform_Go_Live_Date__c` | Date | when used |

### Shared / standard

- `Account.Type`, `Account.ParentId`, Name, billing/shipping address fields as needed for seed realism.

### Do not

- Put `Customer_Id__c` on Location or `Location_Id__c` / `Revenue_Weight__c` on Business.
- Create Opportunities on Location Accounts by default.
- Store raw product telemetry in Salesforce.
- Recreate superseded fields: `Account_Scope__c`, `Branch_Count__c`, `Customer_Segment__c`, `Service_Vertical__c`.

---

## Planned — other CRM objects

| Object | Intent |
|--------|--------|
| Contact | People on Business / Location Accounts |
| Product2 / Asset / Contract | Entitlements and commercial coverage |
| Opportunity | Expansion (and other motions) at Business only; AI linkage fields planned |
| `Account_Signal__c` | Synced deterministic signals for sellers |
| `AI_Recommendation__c` | Draft recommendations for human review |

Planned Opportunity / recommendation field sketches remain in [docs/data-model.md](../../docs/data-model.md).
