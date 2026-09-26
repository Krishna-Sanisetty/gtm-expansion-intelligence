# Recommendation Design

Recommendations are structured, scoped, and optionally abstaining. Commercial action requires a human.

---

## Recommendation scopes

### LOCATION

- Explains a specific location
- Preserves local evidence
- Supporting intelligence for the seller
- **Not** directly actionable as a commercial Opportunity by default

### CUSTOMER

- Aggregates across relevant locations
- Identifies isolated vs systemic patterns
- Considers entitlement coverage and commercial significance
- Recommends rollout scope
- Eligible for human review and Opportunity creation

Only Customer-scoped recommendations create Opportunities.

---

## Entitlement-aware recommendation logic (planned)

Before recommending a product, the system should eventually evaluate:

1. Is the product already entitled?
2. At what scope (Business vs Location)?
3. Is deployment partial?
4. Are affected locations already covered?
5. Is the appropriate action:
   - new product,
   - additional locations,
   - business-wide rollout,
   - or `NO_ACTION`?

Current entitlement source of truth in Salesforce: `Product_Entitlement__c` + Product2 (see [project-context.md](project-context.md)). Do not assume Asset / Contract for the current MVP.

### Planned domain concept: `entitlement_state`

These are analytical / recommendation domain concepts — **not** Salesforce fields unless explicitly requested later.

| Value | Meaning |
|-------|---------|
| `NOT_OWNED` | Product is not active anywhere relevant in the customer hierarchy |
| `PARTIALLY_DEPLOYED` | Product is active for some locations but not others |
| `BUSINESS_WIDE` | Product is active across all relevant / eligible locations |

Implication examples:

- `NOT_OWNED` + strong operational evidence → potential new product expansion.
- `PARTIALLY_DEPLOYED` + affected locations lack coverage → expand rollout to those locations (not a naive “sell the product again”).
- `BUSINESS_WIDE` → generally do not recommend the same product merely because operational signals exist; prefer `NO_ACTION` or a different motion.

Example:

Summit Comfort Group — 12 locations. Contact Center Active in Austin and Dallas; Houston and San Antonio not entitled. Houston and San Antonio show demand / response / conversion pressure.

Prefer: “Expand Contact Center to Houston and San Antonio” (`CUSTOMER`, `MULTI_LOCATION`) over “Sell Contact Center.”

Do not assume Business-level entitlement automatically covers every Location.

---

## Rollout scope (customer recommendations)

| Value | Meaning |
|-------|---------|
| `SINGLE_LOCATION` | One location drives the motion |
| `MULTI_LOCATION` | Several locations share the pattern |
| `BUSINESS_WIDE` | Pattern is systemic across the business |
| `NO_ACTION` | Abstain — do not recommend |

Example: Acme Home Services with Contact Center expansion at Houston + San Antonio → `MULTI_LOCATION`, one parent Expansion Opportunity after acceptance.

---

## Planned recommendation fields

Mark as **planned** until implemented:

| Field | Purpose |
|-------|---------|
| recommended product | What to evaluate |
| recommendation scope | LOCATION / CUSTOMER |
| rollout scope | See above |
| entitlement state | NOT_OWNED / PARTIALLY_DEPLOYED / BUSINESS_WIDE (domain concept) |
| confidence | Model confidence (not a substitute for evidence) |
| affected locations | Explicit list |
| evidence | Structured facts / signals |
| hypothesis | Interpretable claim constrained by evidence |
| why now | Timing rationale |
| discovery questions | Seller prompts |
| seller talk track | Guided selling language |
| next-best action | Concrete next step |
| actionable | Whether commercial action is appropriate |

---

## Actionable flag

Location recommendations are typically non-actionable commercially.

Customer recommendations may be actionable when:

- evidence is sufficient,
- rollout scope is not `NO_ACTION`,
- entitlement / eligibility context supports the motion (coverage checked against `Product_Entitlement__c`).

---

## Evidence and confidence

Evidence must reference verified signals and underlying facts.

Confidence is metadata for the seller — it does not license inventing missing facts.

Unsupported claims should fail evaluation (see [ai-evaluation.md](ai-evaluation.md)).

---

## Abstention

The system must support:

- `RECOMMENDATION`
- `NO_ACTION`

**No recommendation is better than a weak recommendation.**

Prioritize seller trust and precision over volume.

---

## Human gate

Batch syncs recommendations to Salesforce as **Draft**.

Seller accepts → parent Expansion Opportunity (Customer scope only).

Seller dismisses → structured feedback for measurement and future improvement.

See [human-in-the-loop.md](human-in-the-loop.md).
