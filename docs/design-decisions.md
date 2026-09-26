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

**Context:** Sellers live in CRM. Revenue lifecycle (Opportunity → Quote → Order → Contract / Asset) already exists there.

**Decision:** Sync actionable intelligence (signals, AI recommendations) to Salesforce; keep raw telemetry out.

**Consequences:** Custom objects `Account_Signal__c` and `AI_Recommendation__c` are planned. Human review happens in Salesforce.

---

## ADR 6 — Commercial data may be replicated analytically

**Status:** Accepted

**Context:** Entitlements and contracts affect product-gap signals, but Salesforce remains authoritative.

**Decision:** Maintain `entitlement_snapshot` (and similar) in Snowflake as analytical copies with snapshot dates.

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

## Related principles

See the twelve design principles listed in the root [README](../README.md).
