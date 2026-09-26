# Signal Design

Signals are deterministic, typed, and scoped. They sit between raw facts and AI hypotheses.

```text
Raw Fact
→ Location Signal
→ Customer Aggregate Signal
→ AI Hypothesis
→ AI Recommendation (or NO_ACTION)
```

> The model can form a hypothesis. It cannot invent the evidence.

---

## Fact vs signal vs hypothesis

| Kind | Example |
|------|---------|
| **FACT** | Lead volume increased 35%. |
| **FACT** | Response time increased. |
| **FACT** | Conversion declined. |
| **FACT** | Contact Center is not enabled. |
| **DERIVED SIGNAL** | `RESPONSE_TIME_DEGRADING` |
| **DERIVED SIGNAL** | `CONTACT_CENTER_PRODUCT_GAP` |
| **AI HYPOTHESIS** | Inbound demand may be exceeding current operational capacity. |
| **AI RECOMMENDATION** | Investigate whether Contact Center could improve lead handling. |

Facts and signals are produced by Python against Snowflake data. Hypotheses and recommendations are AI outputs constrained by those signals.

---

## Signal scope

### LOCATION

- Explains what is happening at one operating location
- Preserves local evidence
- May identify operational issues or product fit
- Supporting intelligence
- **Not** commercial Opportunity creation by default

Example:

```text
location_id: LOC-101
signal_type: RESPONSE_TIME_DEGRADING
severity: HIGH
```

### CUSTOMER

- Aggregates evidence across relevant locations
- Distinguishes isolated vs systemic patterns
- Considers entitlement coverage and commercial significance
- Eligible for human review and commercial action

Example:

```text
customer_id: CUST-1001
signal_type: WIDESPREAD_RESPONSE_DEGRADATION
severity: HIGH
evidence: 6 of 12 locations affected
```

---

## Example location derivation (illustrative)

For Houston at Acme Home Services, Python would eventually derive signals such as:

- `LEAD_VOLUME_GROWING`
- `RESPONSE_TIME_DEGRADING`
- `CONVERSION_DECLINING`
- `REPEATED_CAPACITY_SUPPORT_ISSUES`
- `CONTACT_CENTER_PRODUCT_GAP`

from measured facts — not from free-form LLM interpretation.

**Rules are not implemented in this foundation pass.** See `signal_engine/signals.py` for documentation-only stubs.

---

## Change detection before AI

After recalculating signals, compare to previous signal state.

If nothing material changed: **stop**. No LLM call. No seller noise.

`No meaningful change → no LLM call → no seller noise.`

---

## Related docs

- [hierarchy-and-aggregation.md](hierarchy-and-aggregation.md)
- [recommendation-design.md](recommendation-design.md)
- [design-decisions.md](design-decisions.md)
