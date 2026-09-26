# Hierarchy and Aggregation

Multi-location customers are the hard case. Flattening too early destroys truth.

> Preserve local evidence. Make commercial decisions at the right business level.

---

## Why branch-aware analysis matters

A parent customer can appear healthy while one location is struggling.

A single noisy branch can also create false urgency for a business-wide expansion motion if averages hide distribution.

Product adoption and entitlements often differ by location (e.g. Contact Center ACTIVE in Austin and Dallas, NOT ENABLED in Houston, San Antonio, Waco).

Recommendations should distinguish:

- product not owned
- partially deployed
- fully deployed

“Expand Contact Center to additional locations” is different from “Sell Contact Center.”

---

## Evaluation order

1. Preserve and score **location-level** evidence
2. Emit location signals / insights
3. Aggregate to **customer-level** signals
4. Decide commercial significance and rollout scope
5. Only then consider Customer-scoped AI recommendation

---

## Isolated vs systemic patterns

| Pattern | Typical rollout |
|---------|-----------------|
| Isolated to one location | `SINGLE_LOCATION` or supporting LOCATION insight |
| Shared by several locations | `MULTI_LOCATION` |
| Widespread across the business | `BUSINESS_WIDE` |
| Weak / ambiguous | `NO_ACTION` |

---

## Aggregation dimensions (planned)

Do not aggregate only by branch count. Future aggregation should support:

- affected location count
- total location count
- percentage of locations affected
- severity distribution
- trend duration
- revenue-weighted impact
- technician-weighted impact
- operational importance
- product entitlement coverage
- geographic clustering

Example customer signal:

```text
WIDESPREAD_RESPONSE_DEGRADATION
Evidence: 6 of 12 locations affected, representing 72% of trailing revenue.
```

---

## Commercial action level

Commercial Opportunities are created at the **CUSTOMER / BUSINESS** (parent Account) level — never by flattening location telemetry into an Opportunity without human review of a Customer recommendation.

Location recommendations remain supporting evidence in the review UI.

---

## Related docs

- [signal-design.md](signal-design.md)
- [recommendation-design.md](recommendation-design.md)
- [data-model.md](data-model.md)
