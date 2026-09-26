"""Deterministic signal generation — design documentation only.

This module describes how location- and customer-scoped signals will be
derived. It intentionally contains no executable rules, thresholds, or
fake implementations.

Core principle
--------------
\"The model can form a hypothesis. It cannot invent the evidence.\"

Python owns operational facts and derived signals. The LLM may interpret
verified signals; it must not invent or recalculate them.

Signal scopes
-------------
LOCATION
    Calculated from a single operating location's telemetry, support facts,
    and entitlement coverage. Preserves local evidence. Supporting
    intelligence — not commercial Opportunity creation by default.

CUSTOMER
    Aggregated from location signals with hierarchy-aware weighting.
    Eligible for human review and commercial action when appropriate.

Conceptual shape
----------------
A signal record will eventually include:

- signal_scope: LOCATION | CUSTOMER
- location_id or customer_id
- signal_type (e.g. RESPONSE_TIME_DEGRADING, WIDESPREAD_RESPONSE_DEGRADATION)
- severity
- evidence (structured facts that justify the signal)
- observed_at / valid_from / valid_to
- model_independent provenance (source metrics, rule version)

Example location signal
-----------------------
location_id: LOC-101
signal_type: RESPONSE_TIME_DEGRADING
severity: HIGH

Example customer signal
-----------------------
customer_id: CUST-1001
signal_type: WIDESPREAD_RESPONSE_DEGRADATION
severity: HIGH
evidence: 6 of 12 locations affected

Planned derivation flow
-----------------------
1. Read changed product usage / support / entitlement facts from Snowflake.
2. Evaluate deterministic rules against location metrics (thresholds,
   trends, product gaps, support patterns).
3. Emit location signals with explicit evidence references.
4. Compare new signal state to previous state; stop early if unchanged.
5. Aggregate location signals into customer signals (coverage, severity
   distribution, revenue/technician weighting, entitlement gaps).
6. Hand verified signals — not raw unstructured blobs — to the AI layer.

Do not implement rules here until the data model and evaluation fixtures
exist. Fake thresholds would invent evidence.
"""
