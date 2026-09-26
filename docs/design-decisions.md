# Design Decisions (ADRs)

Architecture Decision Records for the foundation of GTM Expansion Intelligence.

---

## ADR 1 — Telemetry belongs in Snowflake, not Salesforce

**Status:** Accepted

**Context:** Product usage and support history are high-volume and historical. CRM is a poor store for that shape of data.

**Decision:** Snowflake is the system of analysis for telemetry, support facts, hierarchy snapshots, outcomes, and pipeline state.

**Consequences:** Sellers see intelligence in Salesforce; analysts and batch jobs read Snowflake. Sync is deliberate and narrow.

---

## ADR 2 — Deterministic signal derivation precedes AI reasoning

**Status:** Accepted

**Context:** LLMs are poor sources of operational truth. Thresholds, trends, and product gaps must be reproducible.

**Decision:** Python derives location and customer signals before any model call.

**Consequences:** AI receives verified signals + evidence. Evaluation can test groundedness against known signal sets.

---

## ADR 3 — Preserve location-level evidence

**Status:** Accepted

**Context:** Multi-location customers do not behave uniformly. Early averages hide both risk and opportunity.

**Decision:** Evaluate and store evidence at LOCATION scope before aggregation.

**Consequences:** Location recommendations exist as supporting intelligence; aggregation is explicit and weighted.

---

## ADR 4 — Aggregate upward before commercial recommendation

**Status:** Accepted

**Context:** Commercial Opportunities belong at the parent buying entity, but must be justified by location patterns.

**Decision:** Aggregate location signals to customer signals; only Customer-scoped recommendations are commercially actionable.

**Consequences:** Rollout scopes (`SINGLE_LOCATION`, `MULTI_LOCATION`, `BUSINESS_WIDE`, `NO_ACTION`) become first-class.

---

## ADR 5 — Salesforce is the system of action

**Status:** Accepted

**Context:** Sellers live in CRM. Commercial action (Opportunities) and seller review happen there. Full Quote → Order → Contract → Asset / RLM lifecycle is deferred for the current MVP.

**Decision:** Sync actionable intelligence (signals, AI recommendations) to Salesforce; keep raw telemetry out. Current product ownership context uses Product2 + `Product_Entitlement__c` (see ADR 19).

**Consequences:** Custom objects `Account_Signal__c` and `AI_Recommendation__c` are planned. Human review happens in Salesforce. Do not treat full Revenue Cloud as a prerequisite for the intelligence MVP.

---

## ADR 6 — Commercial data may be replicated analytically

**Status:** Accepted

**Context:** Entitlements affect product-gap signals and recommendation precision, but Salesforce remains authoritative.

**Decision:** Maintain `entitlement_snapshot` (and similar) in Snowflake as analytical copies with snapshot dates, sourced from Salesforce `Product_Entitlement__c` + Product2 — not from Asset / Contract for the current MVP.

**Consequences:** Batch can join usage to coverage without treating Snowflake as commercial system of record.

---

## ADR 7 — Human approval required before Opportunity creation

**Status:** Accepted

**Context:** Auto-creating pipeline from model output destroys trust and pollutes forecasting.

**Decision:** Batch creates Draft AI recommendations only. Sellers accept or dismiss. Accept may create a parent Expansion Opportunity.

**Consequences:** Dismissal reasons and outcomes become measurable feedback.

---

## ADR 8 — Batch processing uses delta detection

**Status:** Accepted

**Context:** Daily full recompute for all customers is wasteful and noisy.

**Decision:** Query for customers/locations changed since last successful watermark; stop if none.

**Consequences:** `pipeline_state` tracks watermarks; idempotent reruns are safe.

---

## ADR 9 — Signal-change detection occurs before an LLM call

**Status:** Accepted

**Context:** LLM cost and seller attention are scarce. Recalculating the same signals should not re-spam recommendations.

**Decision:** Compare new vs previous signal state; invoke AI only on meaningful change.

**Consequences:**

`No meaningful change → no LLM call → no seller noise.`

---

## ADR 10 — AI may abstain

**Status:** Accepted

**Context:** Weak recommendations erode seller trust faster than silence.

**Decision:** Support `RECOMMENDATION` or `NO_ACTION`. Prefer abstention over low-evidence pitches.

**Consequences:** Abstention quality is an explicit evaluation metric.

**No recommendation is better than a weak recommendation.**

---

## ADR 11 — Local-first development, Azure deployment later

**Status:** Accepted

**Context:** Cloud-specific forks create drift and slow iteration.

**Decision:** Implement and test locally; containerize the same code for Azure Container Apps / Jobs later. No Azure-specific business logic.

**Consequences:** `azure/` holds future infra stubs only in this phase.

---

## ADR 12 — Synthetic data only

**Status:** Accepted

**Context:** This is an independent educational / portfolio project.

**Decision:** Use fictional customers, products, metrics, and cases. Never commit real customer or employer-confidential data.

**Consequences:** Offline metrics may be measured on synthetic labels; live business KPIs are documented but not fabricated.

---

## ADR 13 — Account scope uses standard `Account.Type`

**Status:** Accepted (supersedes planned `Account_Scope__c`)

**Context:** Early scaffold docs planned a custom `Account_Scope__c` to distinguish Business vs Location Accounts.

**Decision:** Use standard `Account.Type` with picklist values `Business`, `Location`, and `Other`. FieldPilot sample Accounts use record type `Field_Pilot`.

**Consequences:** Docs and agents must not recreate `Account_Scope__c`. Hierarchy semantics are carried by Type + `ParentId`.

---

## ADR 14 — Business → Location hierarchy via `Account.ParentId`

**Status:** Accepted

**Context:** Multi-location customers need a first-class parent/child Account relationship without inventing a custom hierarchy object.

**Decision:** Location Accounts point to their Business parent with standard `Account.ParentId`. Opportunities are created only on the Business Account.

**Consequences:** Location recommendations stay supporting evidence; commercial action stays at the buying entity.

---

## ADR 15 — Location count uses `NumberofLocations__c`

**Status:** Accepted (supersedes planned `Branch_Count__c`)

**Context:** Scaffold docs planned a custom `Branch_Count__c` for Business location counts.

**Decision:** Repurpose existing Salesforce `NumberofLocations__c` (Number(3,0)) at the Business level.

**Consequences:** Do not introduce `Branch_Count__c`. Aggregation docs refer to `NumberofLocations__c`.

---

## ADR 16 — Separate external IDs for Business and Location

**Status:** Accepted

**Context:** Business and Location need stable external keys for seed loads and Snowflake joins without sharing one Customer ID across scopes.

**Decision:** `Customer_Id__c` (Text(50), External ID) on Business only (e.g. `FP-CUST-1001`); `Location_Id__c` (Text(50), External ID) on Location only (e.g. `FP-LOC-2001`).

**Consequences:** Do not populate `Customer_Id__c` on Location or `Location_Id__c` on Business unless the model is intentionally revised.

---

## ADR 17 — ARR at Business; revenue weight at Location

**Status:** Accepted

**Context:** Branch-level ARR is rarely authoritative; aggregation still needs location commercial significance.

**Decision:** `Customer_ARR__c` is primarily Business-level. `Revenue_Weight__c` (Percent) is Location-level and should total ~100% per Business. Non-active `Location_Status__c` values are excluded from aggregation assumptions.

**Consequences:** Do not invent authoritative Location ARR or put `Revenue_Weight__c` on Business.

---

## ADR 18 — Service verticals are multi-select

**Status:** Accepted (supersedes planned `Service_Vertical__c`)

**Context:** FieldPilot customers may operate multiple trades; a single-select vertical understates reality.

**Decision:** Use `Service_Verticals__c` multi-select (HVAC; Plumbing; Roofing; Electrical; Fencing; Multi-Trade). Segment uses `Segment__c` (SMB | Mid-Market | Enterprise), superseding planned `Customer_Segment__c`.

**Consequences:** Seed CSV multi-select values use semicolon separators. Old single-select / segment field names are historical only.

---

## ADR 19 — Lightweight entitlement model before full revenue lifecycle

**Status:** Accepted

**Context:** The intelligence use case needs reliable product ownership / deployment context. Full Quote → Order → Contract → Asset / Revenue Cloud (RLM) implementation adds substantial complexity not required to validate the core MVP.

**Decision:** Use standard Product2 plus custom `Product_Entitlement__c` as the current entitlement model and source of product-adoption context for the intelligence engine.

**Consequences:**

- Product-gap detection, partial deployment detection, location-aware recommendations, and seller action can proceed without RLM.
- Full Revenue Cloud / RLM lifecycle is **deferred**.
- The lightweight model may later map to or be replaced by standard commercial lifecycle objects if the project expands.
- Do not introduce Asset / Contract / Quote / Order dependencies for entitlement unless explicitly requested.
- Do not duplicate this entitlement model with another custom object without a documented architecture decision.

Authoritative field list: [project-context.md](project-context.md).

---

## ADR 20 — Entitlements are scope-aware

**Status:** Accepted

**Context:** Multi-location customers may deploy products selectively. A parent-level commercial ownership signal is not the same as every branch being enabled.

**Decision:** Entitlements may exist at either Business or Location level on `Product_Entitlement__c.Account__c`. Do not assume Business entitlement means every Location is enabled unless future business logic explicitly defines inheritance.

**Consequences:** Aggregation and recommendations must distinguish `NOT_OWNED`, `PARTIALLY_DEPLOYED`, and `BUSINESS_WIDE` coverage (domain concepts — not Salesforce fields unless requested later).

---

## Related principles

See the twelve design principles listed in the root [README](../README.md).

Authoritative Account, Product, and entitlement field reference: [project-context.md](project-context.md).
