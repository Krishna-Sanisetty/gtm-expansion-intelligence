# Salesforce data model (FieldPilot)

Primary source of truth for Account, Product, and entitlement fields: [docs/project-context.md](../../docs/project-context.md).

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
| Contacts | Seed data implemented in org |

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

## Implemented — Product catalog and entitlements

```text
Product2
    |
    v
Product_Entitlement__c
    |
    +---- Account (Business)
    |
    +---- Account (Location)
```

`Product_Entitlement__c` is the **current** entitlement / product-adoption source for the intelligence MVP. It connects Account + Product2.

Do **not** treat Asset or Contract as the current entitlement source.

### Product2

| Field | Type | Notes |
|-------|------|-------|
| `External_Product_Code__c` | Text(50), External ID | Cross-system product key (e.g. planned codes `FP-CORE`, `FP-CC`, …) |

Product2 **seed records** are planned next — catalog field/model is implemented; do not assume rows are loaded unless confirmed.

### Product_Entitlement__c

| Field | Type | Notes |
|-------|------|-------|
| `Account__c` | Lookup(Account) | Business or Location scope |
| `Product__c` | Lookup(Product2) | Entitled product |
| `Entitlement_Status__c` | Picklist | Active \| Planned \| Suspended |
| `Start_Date__c` | Date | |
| `End_Date__c` | Date | Optional |
| `Annualized_Value__c` | Currency | Optional |
| `Licensed_Quantity__c` | Number | Optional |
| `External_Entitlement_Id__c` | Text(50), External ID | Cross-system entitlement key |

**Scope rules:**

- Entitlements may exist at Business or Location level.
- Do not assume Business entitlement means every Location is enabled.
- Only Active entitlements generally count as current coverage unless future logic says otherwise.

Entitlement **seed records** are planned next.

**Deferred:** Quote / Order / Contract / Asset / full Revenue Cloud (RLM) as the entitlement lifecycle. The lightweight model may later map to those objects if the project expands.

Full narrative and recommendation implications: [docs/project-context.md](../../docs/project-context.md).

---

## Planned / deferred — other CRM objects

| Object | Status | Intent |
|--------|--------|--------|
| Opportunity | Planned | Expansion (and other motions) at Business only; AI linkage fields planned |
| `Account_Signal__c` | Planned | Synced deterministic signals for sellers |
| `AI_Recommendation__c` | Planned | Draft recommendations for human review |
| Quote, Order, Contract, Asset | Deferred | Full commercial / RLM lifecycle — not required for current MVP |

Planned Opportunity / recommendation field sketches remain in [docs/data-model.md](../../docs/data-model.md).
