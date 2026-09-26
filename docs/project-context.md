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

Salesforce will eventually contain:

- customer/account hierarchy,
- Contacts,
- Products,
- product/commercial context,
- Account Signals,
- AI Recommendations,
- seller feedback,
- Opportunities,
- and commercial lifecycle records where practical.

## Current Salesforce Account Model

All FieldPilot sample records use:

Record Type:
`Field_Pilot`

Record Type Id:
`012g7000004KDoPAAW`

### Standard / Repurposed Fields

`Account.Type`

Picklist values:

- Business
- Location
- Other

For this project:

- Business = parent commercial customer
- Location = operating branch

`Account.ParentId`

Used to connect Location Accounts to their parent Business Account.

### Custom / Repurposed Fields

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

If additional picklist values are introduced, document them here.

#### NumberofLocations__c

Number(3,0)

Existing Salesforce field repurposed for the project.

Business-level location count.

## Current Synthetic Account Dataset

Current seed dataset contains:

- 10 Business Accounts
- 50 Location Accounts

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

## Snowflake Role

Snowflake is the `system of analysis`.

Planned analytical datasets include:

- customer,
- customer_location,
- product_usage_fact,
- support_case_fact,
- entitlement_snapshot,
- recommendation_outcome,
- pipeline_state.

Raw historical telemetry belongs in Snowflake rather than Salesforce.

## Product Usage

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

## Signals

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

## AI Recommendations

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

Current order:

1. Salesforce customer hierarchy and Contacts
2. Snowflake schema + synthetic data
3. deterministic signal engine
4. hierarchy aggregation
5. AI structured recommendations
6. RAG
7. Salesforce recommendation writeback
8. human approval / Opportunity action
9. evaluation framework
10. Docker / Azure deployment
11. demo UI

Quoting / contracting / full Revenue Cloud implementation is intentionally deferred because it is not required to validate the core intelligence use case.
