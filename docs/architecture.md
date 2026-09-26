# Architecture

GTM Expansion Intelligence is an evidence-driven post-sales GTM system for a fictional vertical SaaS serving home-services businesses (HVAC, plumbing, electrical, roofing, and similar).

Core flow:

```text
RAW FACTS
→ DETERMINISTIC SIGNALS
→ HIERARCHY-AWARE AGGREGATION
→ AI REASONING
→ HUMAN DECISION
→ COMMERCIAL ACTION
```

Pipeline mnemonic:

`Raw evidence → location signals → business intelligence → AI reasoning → human decision → GTM action`

---

## Source systems

| Source | What it contributes |
|--------|---------------------|
| Operational / product systems | Location-level product telemetry (leads, response time, conversion, jobs, memberships, …) |
| Customer support | Cases, categories, priority, resolution time, CSAT, summaries |
| Salesforce | Commercial hierarchy, entitlements, Opportunities, Quotes, Orders, Contracts, Assets |
| Product documentation (planned RAG corpus) | What products do, eligibility, limitations, relationships |

Sellers cannot manually reconcile these for hundreds of accounts. The architecture keeps each system in its lane.

---

## Snowflake — system of analysis

Snowflake stores analytical snapshots and high-volume history:

- customer and location hierarchy
- product usage facts
- support case facts
- entitlement snapshots (analytical copy)
- recommendation outcomes
- pipeline / watermark state

High-volume historical telemetry does **not** live in Salesforce.

See [data-model.md](data-model.md).

---

## Salesforce — system of action

Salesforce receives actionable intelligence, not raw telemetry:

- Parent Account = commercial customer / buying entity
- Child Account (or equivalent location entity) = branch / location
- Planned custom objects: `Account_Signal__c`, `AI_Recommendation__c`
- Standard commercial objects: Opportunity, Quote, Order, Contract, Asset, Product2

Only **Customer**-scoped recommendations are eligible to create Opportunities after human acceptance.

---

## Python

Python owns:

- delta detection
- deterministic signal derivation
- location-level calculation
- cross-location aggregation
- signal-change detection
- orchestration
- API services
- typed schemas
- evaluation logic

Packages in this repo:

| Package | Role |
|---------|------|
| `backend/` | FastAPI services |
| `batch/` | Daily orchestration |
| `signal_engine/` | Deterministic signals + aggregation |
| `ai/` | Recommendation orchestration, RAG, evaluation |

---

## AI / LLM

AI interprets **verified** signals. It may:

- retrieve product knowledge
- form hypotheses
- explain recommendations
- generate discovery questions and talk tracks
- recommend next-best actions
- abstain (`NO_ACTION`)

AI must **not** invent operational facts.

> The model can form a hypothesis. It cannot invent the evidence.

---

## Azure (planned runtime)

Development is local-first. The same implementation should later be containerized and deployed to Azure.

Preferred future services: Container Apps, Container Apps Jobs, Azure OpenAI, AI Search, Key Vault, Monitor / Application Insights.

Do **not** build Azure-specific business logic or fork local vs cloud implementations.

---

## Scheduled vs synchronous

| Mode | Use |
|------|-----|
| **Scheduled batch** (primary) | Daily delta → signals → optional AI → Salesforce Draft recommendations |
| **Synchronous API** (planned) | Health, inspection, review helpers, demo endpoints |

Batch principle:

`No meaningful change → no LLM call → no seller noise.`

---

## Local-to-cloud deployment

1. Run locally (`uvicorn`, `python -m batch.run`)
2. Validate against synthetic data
3. Containerize (`docker/`)
4. Deploy the same image to Azure Container Apps / Jobs
5. Externalize secrets via Key Vault (planned)

See also [design-decisions.md](design-decisions.md).
