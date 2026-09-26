# Data Model

Analytical model in Snowflake; commercial authority in Salesforce. This document is the planned schema — **DDL is not implemented yet**.

---

## Hierarchy

| Level | Meaning |
|-------|---------|
| **CUSTOMER / BUSINESS** | Parent commercial entity. Primary Salesforce Account. Opportunities live here. |
| **LOCATION / BRANCH** | Operating location under the customer. Product usage, support, and entitlements may differ. |

Do not flatten location telemetry into a single account average too early.

**Preserve local evidence. Make commercial decisions at the right business level.**

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

## Salesforce objects (planned)

### Standard objects

Account, Contact, Product2, Asset, Contract, Opportunity, Quote, Order.

Parent Account = customer/business. Child Account (or equivalent) = location/branch.

### Planned Account fields

| Field | Notes |
|-------|-------|
| `Customer_ID__c` | Text, Unique, External ID |
| `Customer_Segment__c` | |
| `Service_Vertical__c` | |
| `Technician_Count__c` | |
| `Branch_Count__c` | |
| `Customer_ARR__c` | |
| `Customer_Health_Score__c` | |
| `Platform_Go_Live_Date__c` | |
| `Customer_Status__c` | |

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
