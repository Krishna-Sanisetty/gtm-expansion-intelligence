# Project

Project:
`GTM Expansion Intelligence`

Fictional company:
`FieldPilot`

Domain:
Vertical SaaS serving home-services businesses such as HVAC, plumbing, electrical, roofing, fencing, and multi-trade operators.

Primary use case:
Post-sales expansion intelligence.

The system combines:

- product telemetry,
- customer support activity,
- Salesforce commercial/customer context,
- product entitlements,
- hierarchy information,
- and product knowledge

to determine where meaningful expansion opportunities may exist.

## Customer Hierarchy

There are two primary Account scopes.

### Business

Represents the parent commercial customer / buying entity.

Commercial Opportunities are created at this level.

### Location

Represents an operating location / branch belonging to a Business Account.

Product usage, support behavior, technician counts, product adoption, and operational performance can vary by location.

The system must preserve location-level evidence before aggregating to the Business.

Location intelligence supports customer-level recommendations.

Location recommendations are not directly commercially actionable by default.

Customer-level recommendations may become commercial Opportunities after human approval.

Use standard Salesforce `Account.ParentId` to represent the Business → Location hierarchy.

## Intelligence Hierarchy

Raw facts
→ deterministic location signals
→ location intelligence
→ cross-location aggregation
→ customer-level signals
→ AI customer recommendation
→ human review
→ parent-level Opportunity

Do not flatten all branch telemetry into parent-level averages before deriving location signals.

## Salesforce Role

Salesforce is the seller-facing `system of action`.

Do not store high-volume raw telemetry in Salesforce.

Salesforce currently contains (implemented):

- Business and Location Accounts,
- Contacts,
- Product2 (product catalog),
- Product_Entitlement__c (lightweight entitlement / product-adoption context),
- and the Account hierarchy model documented below.

Salesforce will eventually also contain:

- Account Signals,
- AI Recommendations,
- seller feedback,
- Opportunities,
- and (deferred) full commercial lifecycle records (Quote / Order / Contract / Asset / RLM) if the project expands.

Salesforce remains authoritative for current entitlement state.

## Salesforce Account Model — Implemented

**Status: Implemented** (FieldPilot org + synthetic seed). This section is the authoritative Account field list. Do not document or recreate the superseded planned names `Account_Scope__c`, `Branch_Count__c`, `Customer_Segment__c`, or `Service_Vertical__c`.

Architecture rules that are also implemented:

- Hierarchy uses standard `Account.ParentId` (Business → Location).
- Opportunities are created at the **Business** Account only.
- `Customer_Id__c` is Business-only; `Location_Id__c` is Location-only.
- `Revenue_Weight__c` is Location-level; `Customer_ARR__c` is primarily Business-level.
- `NumberofLocations__c` is Business-level.
- Do not store raw product telemetry in Salesforce.

All FieldPilot sample records use:

Record Type:
`Field_Pilot`

Record Type Id:
`012g7000004KDoPAAW`

### Standard / Repurposed Fields (Implemented)

`Account.Type`

Picklist values:

- Business
- Location
- Other

For this project:

- Business = parent commercial customer
- Location = operating branch

Supersedes the earlier planned custom field `Account_Scope__c`.

`Account.ParentId`

Used to connect Location Accounts to their parent Business Account.

### Custom / Repurposed Fields (Implemented)

#### Customer_Id__c

Type:
Text(50), External ID

Meaning:
Unique identifier assigned when a Business becomes a FieldPilot customer.

Usage:
Business records only.

Example:
`FP-CUST-1001`

Do not populate this field on Location records unless the data model is intentionally revised later.

#### Location_Id__c

Type:
Text(50), External ID

Meaning:
Unique FieldPilot identifier assigned to an operating location.

Usage:
Location records only.

Example:
`FP-LOC-2001`

#### Segment__c

Picklist:

- SMB
- Mid-Market
- Enterprise

Used on Business and Location records.

Supersedes the earlier planned name `Customer_Segment__c`.

#### Service_Verticals__c

Multi-select picklist.

Values:

- HVAC
- Plumbing
- Roofing
- Electrical
- Fencing
- Multi-Trade

Salesforce multi-select CSV values use semicolon separators.

Supersedes the earlier planned single-select `Service_Vertical__c`.

#### Platform_Go_Live_Date__c

Type:
Date

Represents when the customer became operational on FieldPilot.

Primarily used for tenure/lifecycle context.

#### Customer_Status__c

Picklist:

- Prospect
- Onboarding
- Active
- At Risk
- Churned

Used to determine whether a Business is an appropriate expansion candidate.

#### Technician_Count__c

Number(8,0)

Business:
total technician count across its locations.

Location:
technicians associated with that branch.

For synthetic test data, Business technician count should equal the sum of its Location records.

#### Customer_ARR__c

Currency(16,2)

Use primarily at Business level.

Do not invent authoritative branch-level ARR unless specifically required later.

#### Revenue_Weight__c

Percent(5,2)

Location-level weighting showing the approximate commercial/operational significance of a location within the Business.

Location revenue weights should total approximately 100% per Business.

Used later during hierarchy aggregation.

Do not treat this as a Business-level field.

#### Customer_Health_Score__c

Number(3,0)

Synthetic contextual score from 0–100.

May be used as supporting context later.

The AI must not treat this single field as authoritative evidence.

#### Location_Status__c

Picklist.

Used on Location records to prevent inactive/closed locations from contaminating signal calculations.

Current synthetic data may include:

- Active
- Opening

Non-active locations are excluded from aggregation assumptions unless explicitly revisited.

If additional picklist values are introduced, document them here.

#### NumberofLocations__c

Number(3,0)

Existing Salesforce field repurposed for the project.

Business-level location count.

Supersedes the earlier planned custom field `Branch_Count__c`.

### Name mapping (stale → implemented)

| Stale / planned (do not use) | Implemented |
|------------------------------|-------------|
| `Account_Scope__c` | `Account.Type` (`Business` / `Location` / `Other`) |
| `Branch_Count__c` | `NumberofLocations__c` |
| `Customer_Segment__c` | `Segment__c` |
| `Service_Vertical__c` | `Service_Verticals__c` (multi-select) |

## Current Synthetic Account Dataset

Current seed dataset contains:

- 10 Business Accounts
- 50 Location Accounts
- Contact seed data (implemented in the org)

The dataset intentionally includes:

- SMB,
- Mid-Market,
- Enterprise,
- single/multi-trade businesses,
- varying technician counts,
- varying ARR,
- varying health,
- varying location weights,
- Active,
- At Risk,
- Onboarding customers,
- and an Opening branch.

Seed files:

- `fieldpilot_account_seed_data.xlsx`
- `fieldpilot_business_accounts.csv`
- `fieldpilot_location_accounts.csv`

If these files are not stored in the repository, do not assume they are available locally.

Product2 catalog seed records and Product_Entitlement__c seed records are **planned / next** — do not mark those data loads complete unless they are actually present.

## Implemented Product & Entitlement Model

**Status: Implemented** (FieldPilot org — object/field model created manually). This section is authoritative for the current product catalog and entitlement source. Do not reintroduce Asset / Contract / Quote / Order / Revenue Cloud as required for the current MVP.

### Why this model exists

The project originally considered full Salesforce Revenue Cloud / RLM objects (Quote, Order, Contract, Asset). Implementing the complete commercial lifecycle adds substantial complexity that is not necessary to validate the core GTM intelligence use case.

The current MVP therefore uses:

`Product2` + `Product_Entitlement__c`

to answer:

- What products does the customer currently use?
- Which products are missing?
- Is a product deployed business-wide or only at selected locations?
- Which affected locations do not have the recommended product?
- Is the recommendation a new product sale or an expansion of an existing deployment?

Full quoting / contracting / ordering remains a **deferred / future** enhancement. Do not treat RLM as a prerequisite for the current project.

### Product2 (Implemented)

Standard Salesforce product catalog.

#### External_Product_Code__c

Type:
Text(50), External ID

Purpose:
Stable product identifier across Salesforce, Snowflake, Python services, RAG/product knowledge, and synthetic seed data.

Planned FieldPilot product codes (fictional / synthetic — do not imply affiliation with any real vendor):

| Code | Product |
|------|---------|
| `FP-CORE` | Core CRM & FSM |
| `FP-DISP` | Advanced Dispatch |
| `FP-CC` | Contact Center |
| `FP-MKT` | Marketing Automation |
| `FP-FS` | Field Sales |
| `FP-MEM` | Memberships |
| `FP-PAY` | Payments |
| `FP-REV` | Revenue Intelligence |

Product2 **seed records** for these codes are planned next work — the field and catalog model are implemented; do not assume catalog rows are loaded unless confirmed.

### Product_Entitlement__c (Implemented)

Lightweight custom object. Current source of product-adoption / entitlement context for the intelligence engine.

Purpose:
Represent which FieldPilot products are enabled / entitled for a Business or Location Account without requiring the full Revenue Cloud lifecycle.

#### Implemented fields

| Field | Type | Meaning |
|-------|------|---------|
| `Account__c` | Lookup(Account) | Business or Location Account that owns / is enabled for the product |
| `Product__c` | Lookup(Product2) | FieldPilot product associated with the entitlement |
| `Entitlement_Status__c` | Picklist | Current commercial/operational status |
| `Start_Date__c` | Date | Date the entitlement became or becomes active |
| `End_Date__c` | Date (optional) | End / expiry date where applicable |
| `Annualized_Value__c` | Currency (optional) | Synthetic commercial value; not required for all entitlements |
| `Licensed_Quantity__c` | Number (optional) | Synthetic licensed quantity / capacity where relevant; some products may not use a meaningful quantity |
| `External_Entitlement_Id__c` | Text(50), External ID | Stable entitlement identifier across systems |

Intended `Entitlement_Status__c` values:

- `Active`
- `Planned`
- `Suspended`

Only **Active** entitlements should generally count as currently enabled product coverage unless future business logic says otherwise.

Example external ID convention (for later seed work only — do not invent actual seed IDs here):

`FP-ENT-0001`

#### Entitlement scope and hierarchy

Entitlements may exist at either:

- **Business** scope, or
- **Location** scope

Hierarchy remains Business → Location.

Do **not** assume a Business-level entitlement means every child Location is enabled unless future business logic explicitly defines inheritance.

Examples:

Business-level:

```text
Acme Home Services → Payments → Active
```

Location-level (partial deployment):

```text
Acme - Austin  → Contact Center → Active
Acme - Dallas  → Contact Center → Active
Acme - Houston → Contact Center → not entitled
```

#### Coverage states (domain concepts — not Salesforce fields)

The intelligence engine must eventually determine:

| Concept | Meaning | Typical recommendation implication |
|---------|---------|-----------------------------------|
| `NOT_OWNED` | Product is not active anywhere relevant in the customer hierarchy | New product expansion |
| `PARTIALLY_DEPLOYED` | Product is active for some locations but not others | Expand rollout to additional locations |
| `BUSINESS_WIDE` | Product is active across all relevant/eligible locations | Do not recommend the same product merely because operational signals exist |

These are analytical / recommendation domain concepts. Do not create Salesforce fields for them unless explicitly requested later.

#### Entitlement-aware recommendations

The AI recommendation layer must not recommend a product without checking entitlement coverage.

Example:

Business: Summit Comfort Group (12 locations)

Contact Center entitlements: Austin Active, Dallas Active; Houston and San Antonio not entitled.

Operational evidence: Houston and San Antonio show growing inbound demand, worsening response time, declining conversion.

Correct interpretation is not merely “Sell Contact Center.” It may instead be:

“Expand Contact Center to Houston and San Antonio.”

Customer-level recommendation shape:

- Recommendation Scope: `CUSTOMER`
- Rollout Scope: `MULTI_LOCATION`
- Affected / recommended locations: Houston, San Antonio
- Commercial action: one parent-level Expansion Opportunity after human approval

Location-level intelligence remains supporting evidence.

## Snowflake Role — Planned

Snowflake is the `system of analysis`.

**Status: Planned** (schema + synthetic loads not yet shipped in-repo).

Planned analytical datasets include:

- customer,
- customer_location,
- product_usage_fact,
- support_case_fact,
- entitlement_snapshot,
- recommendation_outcome,
- pipeline_state.

Raw historical telemetry belongs in Snowflake rather than Salesforce.

### Planned entitlement_snapshot source

Planned Snowflake `entitlement_snapshot` should be sourced from Salesforce:

`Product_Entitlement__c` + `Product2`

not from Asset / Contract.

Salesforce remains authoritative for current entitlement state. Snowflake may hold a replicated analytical snapshot for efficient batch analysis.

Planned analytical fields may include:

- `customer_id`
- `location_id`
- `external_entitlement_id`
- `product_code`
- `entitlement_status`
- `start_date`
- `end_date`
- `annualized_value`
- `licensed_quantity`
- `snapshot_date`

Do not implement the table in this documentation task unless it already exists.

## Product Usage — Planned

Product usage should eventually be captured at location level where applicable.

Example metrics:

- inbound leads,
- average lead response minutes,
- lead conversion rate,
- unsold estimates,
- active memberships,
- jobs completed.

## Customer Support

Synthetic support data will also be loaded into Snowflake.

Support cases may be:

- location-specific,
- or parent/customer-level when location cannot be attributed.

Support activity contributes evidence but does not itself automatically trigger a commercial recommendation.

## Signals — Planned

Signals are deterministic.

Example location signals:

- LEAD_VOLUME_GROWING
- RESPONSE_TIME_DEGRADING
- CONVERSION_DECLINING
- UNSOLD_ESTIMATES_GROWING
- REPEATED_CAPACITY_SUPPORT_ISSUES
- PRODUCT_GAP_CONTACT_CENTER

Signals should support scope:

- LOCATION
- CUSTOMER

Customer signals are created by aggregating location evidence.

Aggregation may eventually consider:

- affected location count,
- percentage of locations affected,
- severity,
- duration,
- revenue weight,
- technician weight,
- entitlement coverage,
- geographic concentration.

## AI Recommendations — Planned

AI recommendations may exist at two scopes.

### Location Recommendation

Purpose:
Explain local evidence and possible product-fit hypothesis.

Commercial action:
Not actionable by default.

### Customer Recommendation

Purpose:
Aggregate relevant location evidence into a parent-level commercial recommendation.

Commercial action:
Eligible for human review.

Only an accepted Customer recommendation should create an Expansion Opportunity.

Potential rollout scopes:

- SINGLE_LOCATION
- MULTI_LOCATION
- BUSINESS_WIDE
- NO_ACTION

## Human In The Loop

The batch/AI pipeline must not automatically create commercial Opportunities.

Expected flow:

AI Recommendation
→ seller reviews evidence
→ Accept or Dismiss

Accept:
may create parent-level Expansion Opportunity.

Dismiss:
capture structured feedback.

## Batch Philosophy

Local development first.

Initial execution should eventually support:

`python -m batch.run`

The production-style version will later use the same code in Azure.

Processing principle:

Changed source data?
→ No → stop.

Changed?
→ recalculate deterministic signals.

Meaningful signal change?
→ No → stop.

Changed?
→ invoke AI recommendation process.

Use this rule:

`No meaningful change → no LLM call → no seller noise.`

## AI Principle

Use this as a core system constraint:

`The model can form a hypothesis. It cannot invent the evidence.`

Facts and deterministic calculations must come from source data / deterministic Python logic.

The LLM is used for:

- interpretation,
- hypothesis formation,
- retrieval-grounded product fit,
- explanation,
- discovery questions,
- talk tracks,
- next-best actions.

## Measurement

Success is measured across three layers.

### Technical / AI Quality

- recommendation precision
- groundedness
- unsupported claim rate
- retrieval relevance
- structured output validity
- latency
- cost
- reliability
- abstention quality

### Seller Workflow

- recommendation review rate
- acceptance rate
- dismissal reasons
- opportunity creation
- research time saved

### Business Outcome

- expansion pipeline
- win rate
- expansion ARR
- account coverage
- seller productivity

Do not fabricate production business results for this portfolio project.

## Cloud Strategy

Build and validate locally first.

Later:

- Dockerize the same implementation.
- Deploy scheduled/background processing to Azure.
- Do not create separate cloud-specific business logic.

Likely future Azure components may include:

- Azure Container Apps
- Azure Container Apps Jobs
- Azure OpenAI
- Azure AI Search
- Key Vault
- Azure Monitor / Application Insights

These are planned, not necessarily implemented.

## Current Development Priority

Salesforce foundation now includes:

1. Account hierarchy (**implemented**)
2. Contacts (**implemented**)
3. Product catalog model — Product2 + `External_Product_Code__c` (**implemented**)
4. Product entitlement model — `Product_Entitlement__c` (**implemented**)

Next major data / modeling work (planned — not complete unless confirmed):

- Product2 seed records
- Product_Entitlement__c seed records
- Snowflake analytical schema / synthetic telemetry / support data

Broader delivery order:

1. Product2 + entitlement seed data (next)
2. Snowflake schema + synthetic telemetry / support data
3. deterministic signal engine
4. hierarchy aggregation (including entitlement coverage)
5. AI structured recommendations (entitlement-aware)
6. RAG
7. Salesforce recommendation writeback
8. human approval / Opportunity action
9. evaluation framework
10. Docker / Azure deployment
11. demo UI

**Deferred:** complete RLM quoting / ordering / contracting lifecycle (Quote → Order → Contract → Asset). Not required to validate the core intelligence use case.
