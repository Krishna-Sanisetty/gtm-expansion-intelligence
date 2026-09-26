# Hierarchy and Aggregation

Multi-location customers are the hard case. Flattening too early destroys truth.

> Preserve local evidence. Make commercial decisions at the right business level.

---

## Salesforce hierarchy (implemented)

| Role | How it is modeled |
|------|-------------------|
| Business (parent) | `Account.Type = Business`; `Customer_Id__c`; `NumberofLocations__c`; primarily `Customer_ARR__c` |
| Location (child) | `Account.Type = Location`; `Account.ParentId` → Business; `Location_Id__c`; `Revenue_Weight__c`; `Location_Status__c` |

Rules:

- Commercial Opportunities are created at the **Business** Account only.
- Location recommendations remain supporting evidence; they are not commercially actionable by default.
- Aggregation should respect `Revenue_Weight__c` and exclude non-active `Location_Status__c` values (synthetic data uses Active / Opening; Opening is treated as non-active for aggregation assumptions).
- Do not put `Customer_Id__c` on Location or `Revenue_Weight__c` on Business.

Authoritative field list: [project-context.md](project-context.md).

---

## Why branch-aware analysis matters

A parent customer can appear healthy while one location is struggling.

A single noisy branch can also create false urgency for a business-wide expansion motion if averages hide distribution.

Product adoption and entitlements often differ by location (e.g. Contact Center Active in Austin and Dallas, not entitled in Houston, San Antonio, Waco).

Current entitlement source: Salesforce `Product_Entitlement__c` (Business or Location scope). Do not assume Business entitlement means every Location is enabled.

Recommendations should distinguish:

- product not owned (`NOT_OWNED`)
- partially deployed (`PARTIALLY_DEPLOYED`)
- business-wide / fully deployed (`BUSINESS_WIDE`)

“Expand Contact Center to additional locations” is different from “Sell Contact Center.”

---

## Evaluation order

1. Preserve and score **location-level** evidence
2. Emit location signals / insights
3. Aggregate to **customer-level** signals
4. Combine with **product-coverage / entitlement** aggregation
5. Decide commercial significance and rollout scope
6. Only then consider Customer-scoped AI recommendation

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

Do not aggregate only by location count (`NumberofLocations__c`). Future aggregation should support:

- affected location count
- total location count (`NumberofLocations__c` at Business)
- percentage of locations affected
- severity distribution
- trend duration
- revenue-weighted impact (`Revenue_Weight__c`)
- technician-weighted impact (`Technician_Count__c`)
- operational importance
- product entitlement coverage (from `Product_Entitlement__c`)
- location status (`Location_Status__c`)
- geographic clustering

### Product-coverage aggregation

Customer-level intelligence should eventually combine:

- affected locations,
- location severity,
- revenue weights,
- technician weights,
- entitlement coverage,
- location status.

Example:

```text
8 of 12 locations affected.
6 affected locations do not have Contact Center.
2 affected locations already have Contact Center.
```

This should produce a more precise rollout recommendation (expand to the uncovered affected locations) than simply “recommend Contact Center.”

Example customer signal (severity / weight):

```text
WIDESPREAD_RESPONSE_DEGRADATION
Evidence: 6 of 12 locations affected, representing 72% of trailing revenue.
```

Entitlement coverage must refine product recommendations after signal aggregation — not replace operational evidence.

## Commercial action level

Commercial Opportunities are created at the **CUSTOMER / BUSINESS** (parent Account, `Account.Type = Business`) level — never by flattening location telemetry into an Opportunity without human review of a Customer recommendation.

Location recommendations remain supporting evidence in the review UI.

---

## Related docs

- [project-context.md](project-context.md)
- [signal-design.md](signal-design.md)
- [recommendation-design.md](recommendation-design.md)
- [data-model.md](data-model.md)
