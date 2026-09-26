# Data Model

Analytical model in Snowflake; commercial authority in Salesforce. This document is the planned schema — **DDL is not implemented yet**.

---

## Hierarchy

| Level | Meaning | Salesforce |
|-------|---------|------------|
| **CUSTOMER / BUSINESS** | Parent commercial entity. Opportunities live here. | `Account.Type = Business`; `Customer_Id__c`; `NumberofLocations__c`; primarily `Customer_ARR__c` |
| **LOCATION / BRANCH** | Operating location under the customer. Product usage, support, and entitlements may differ. | `Account.Type = Location`; `Account.ParentId` → Business; `Location_Id__c`; `Revenue_Weight__c`; `Location_Status__c` |

Hierarchy link: standard `Account.ParentId` (Location → Business). Do not flatten location telemetry into a single account average too early.

**Preserve local evidence. Make commercial decisions at the right business level.**

Authoritative FieldPilot Account field detail: [project-context.md](project-context.md).

---

## Snowflake tables (planned)

### `customer`

Parent commercial entity.

| Field | Notes |
|-------|-------|
| `customer_id` | Primary key |
| `customer_name` | |
| `segment` | |
| `vertical` | e.g. HVAC, plumbing |
| `status` | |
| `annual_revenue` | |
| `customer_arr` | |
| `created_at` | |
| `updated_at` | |

### `customer_location`

Operating locations.

| Field | Notes |
|-------|-------|
| `location_id` | Primary key |
| `customer_id` | FK → customer |
| `location_name` | |
| `city` | |
| `state` | |
| `status` | |
| `technician_count` | For weighted impact |
| `employee_count` | |
| `revenue_weight` | For revenue-weighted aggregation |
| `created_at` | |
| `updated_at` | |

### `product_usage_fact`

| Field | Notes |
|-------|-------|
| `customer_id` | |
| `location_id` | |
| `metric_date` | |
| `metric_name` | |
| `metric_value` | |
| `source_system` | |
| `updated_at` | |

Example metrics: `INBOUND_LEADS`, `AVG_LEAD_RESPONSE_MIN`, `LEAD_CONVERSION_RATE`, `UNSOLD_ESTIMATES`, `ACTIVE_MEMBERSHIPS`, `JOBS_COMPLETED`.

### `support_case_fact`

| Field | Notes |
|-------|-------|
| `customer_id` | |
| `location_id` | May be NULL for customer-level cases |
| `case_id` | |
| `created_at` | |
| `case_category` | |
| `case_subcategory` | |
| `priority` | |
| `resolution_time_hours` | |
| `csat_score` | |
| `case_status` | |
| `case_summary` | |
| `source_system` | |

### `entitlement_snapshot`

Analytical copy of Salesforce commercial context. Salesforce remains system of record.

| Field | Notes |
|-------|-------|
| `customer_id` | |
| `location_id` | Distinguishes partial vs full deployment |
| `product_code` | |
| `contract_id` | |
| `contract_start_date` | |
| `contract_end_date` | |
| `annual_value` | |
| `quantity` | |
| `status` | e.g. ACTIVE, NOT ENABLED |
| `snapshot_date` | |

### `recommendation_outcome`

| Field | Notes |
|-------|-------|
| `recommendation_id` | |
| `customer_id` | |
| `recommended_product` | |
| `generated_at` | |
| `accepted` | |
| `dismissal_reason` | |
| `opportunity_created` | |
| `opportunity_id` | |
| `pipeline_amount` | |
| `closed_won` | |
| `closed_won_amount` | |
| `model_version` | |
| `prompt_version` | |

### `pipeline_state`

| Field | Notes |
|-------|-------|
| `pipeline_name` | |
| `last_successful_run` | |
| `last_watermark` | |
| `updated_at` | |

---

## Salesforce objects

### Standard objects

Account, Contact, Product2, Asset, Contract, Opportunity, Quote, Order.

- Business Account (`Account.Type = Business`) = commercial customer / buying entity.
- Location Account (`Account.Type = Location`) = operating branch, linked via `Account.ParentId`.
- Opportunities belong on the Business Account only.
- Record type for FieldPilot sample Accounts: `Field_Pilot` (`012g7000004KDoPAAW`).

### Implemented Account fields

**Status: Implemented.** See [project-context.md](project-context.md) for full definitions. Do not use the superseded names `Account_Scope__c`, `Branch_Count__c`, `Customer_Segment__c`, or `Service_Vertical__c`.

| Field | Scope | Notes |
|-------|-------|-------|
| `Account.Type` | Business / Location / Other | Replaces planned `Account_Scope__c` |
| `Account.ParentId` | Location → Business | Standard hierarchy |
| `Customer_Id__c` | Business only | Text(50), External ID; e.g. `FP-CUST-1001` |
| `Location_Id__c` | Location only | Text(50), External ID; e.g. `FP-LOC-2001` |
| `Segment__c` | Business and Location | SMB \| Mid-Market \| Enterprise (replaces `Customer_Segment__c`) |
| `Service_Verticals__c` | Business and Location | Multi-select (replaces `Service_Vertical__c`) |
| `Platform_Go_Live_Date__c` | primarily Business | Date |
| `Customer_Status__c` | primarily Business | Prospect \| Onboarding \| Active \| At Risk \| Churned |
| `Technician_Count__c` | Business and Location | Number(8,0); Business = sum of locations in synthetic data |
| `Customer_ARR__c` | primarily Business | Currency(16,2) |
| `Revenue_Weight__c` | Location only | Percent(5,2); ~100% per Business |
| `Customer_Health_Score__c` | supporting context | Number(3,0) 0–100; not authoritative evidence |
| `Location_Status__c` | Location | Active / Opening in synthetic data; non-active excluded from aggregation assumptions |
| `NumberofLocations__c` | Business | Number(3,0); repurposed standard field (replaces `Branch_Count__c`) |

Synthetic seed: **10 Business + 50 Location** Accounts.

### Planned Product2 / Asset / Opportunity fields

| Object | Field | Notes |
|--------|-------|-------|
| Product2 | `External_Product_Code__c` | |
| Asset | `External_Entitlement_ID__c` | |
| Asset | `Licensed_Quantity__c` | |
| Asset | `Annualized_Value__c` | |
| Opportunity | `Opportunity_Motion__c` | New Logo, Expansion, Renewal, Reactivation |
| Opportunity | `AI_Generated__c` | |
| Opportunity | `AI_Recommendation_ID__c` | |

### Planned custom objects

**`Account_Signal__c`** — actionable signal records synced for seller context.

**`AI_Recommendation__c`** — Draft recommendations for human review. Planned fields include:

| Field | Values / notes |
|-------|----------------|
| `Recommendation_Scope__c` | Location, Customer |
| `Actionable__c` | |
| `Rollout_Scope__c` | Single Location, Multi Location, Business Wide, No Action |
| `Status__c` | Draft, Presented, Accepted, Dismissed, Converted, Expired |
| `Seller_Feedback__c` | |
| `Reviewed_At__c` | |
| `Converted_Opportunity__c` | |
| `Recommended_Product__c` | |
| `Confidence__c` | |
| `Why_Now__c` | |
| `Talk_Track__c` | |
| `Discovery_Questions__c` | |
| `Evidence_JSON__c` | |
| `Model_Name__c` | |
| `Prompt_Version__c` | |
| `Generated_At__c` | |

Only Customer recommendations should be eligible to create a commercial Opportunity.
