# Success Metrics

Success is **not** “the LLM returned an answer.”

Design measurement across three layers. This is a synthetic portfolio project — do not fabricate business results. Offline evaluation may report measured results from synthetic labeled data. Production KPIs below are **intended** live measurements.

---

## Layer 1 — AI / technical quality

- recommendation precision
- groundedness
- unsupported claim rate
- retrieval relevance
- structured-output validity
- latency
- cost
- reliability
- task completion
- abstention quality

See [ai-evaluation.md](ai-evaluation.md).

---

## Layer 2 — Seller workflow

- recommendation review rate
- recommendation acceptance rate
- dismissal rate
- dismissal reason distribution
- opportunity creation rate
- seller engagement
- research time saved

Feedback captured in Salesforce review (see [human-in-the-loop.md](human-in-the-loop.md)) should land in `recommendation_outcome` analytically.

---

## Layer 3 — Business outcomes

- AI-sourced pipeline
- AI-influenced pipeline
- expansion opportunity win rate
- closed-won expansion ARR
- incremental expansion revenue
- account coverage
- seller productivity

These are documented as metrics that would be measured in a live deployment. They will not be invented for demos.

---

## Design implication

Precision and abstention quality protect Layers 2 and 3. Flooding sellers with weak recommendations destroys trust even if Layer 1 “task completion” looks high.

**No recommendation is better than a weak recommendation.**
