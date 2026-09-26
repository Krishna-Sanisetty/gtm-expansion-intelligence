# Human in the Loop

The batch process must **not** automatically create commercial Opportunities.

It creates AI recommendations. Humans decide commercial action.

---

## Salesforce workflow (planned)

```text
AI Recommendation
Status = Draft
        │
        ▼
Seller reviews
  - recommendation
  - evidence
  - affected locations
  - why now
  - confidence
  - discovery questions
  - talk track
  - suggested rollout scope
        │
   ┌────┴────┐
   ▼         ▼
ACCEPT     DISMISS
   │         │
   ▼         ▼
Create       Capture
parent-level structured
Expansion    feedback
Opportunity
```

---

## Accept

If the seller accepts a **Customer**-scoped actionable recommendation:

- Create one parent-level Expansion Opportunity
- Link `AI_Recommendation_ID__c` / `Converted_Opportunity__c`
- Set recommendation status to Accepted / Converted as appropriate

Location recommendations remain supporting evidence and are not directly Opportunity-creating by default.

---

## Dismiss

Capture structured feedback. Suggested dismissal reasons:

- Wrong Product
- Bad Timing
- Incorrect Evidence
- Already In Progress
- Customer Not Eligible
- Not Relevant
- Other

Dismissal feeds measurement (Layer 2) and future evaluation datasets.

---

## Principles

- AI proposes; sellers decide
- Precision over volume
- Explainability is mandatory — evidence must be inspectable
- Outcomes and feedback flow back to Snowflake for learning and KPI tracking

See [success-metrics.md](success-metrics.md) and [recommendation-design.md](recommendation-design.md).
