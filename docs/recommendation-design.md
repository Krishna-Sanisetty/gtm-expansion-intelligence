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
- entitlement / eligibility context supports the motion.

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
