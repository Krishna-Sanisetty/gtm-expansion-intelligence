# AI Evaluation

Offline evaluation proves whether recommendations are grounded and useful. Production business KPIs are separate (see [success-metrics.md](success-metrics.md)).

This project is synthetic. Do **not** fabricate live business results. Offline evaluation may report real measured results from labeled synthetic data.

---

## What we evaluate

| Dimension | Question |
|-----------|----------|
| **Precision** | When we recommend, are we right often enough for seller trust? |
| **Groundedness** | Does every claim map to verified signals / retrieved docs? |
| **Unsupported claims** | Did the model invent facts not present in evidence? |
| **Retrieval quality** | Were the right product docs retrieved for the motion? |
| **Schema validity** | Did structured output match the contract? |
| **Latency** | Is batch / interactive latency acceptable? |
| **Cost** | Token / embedding cost per changed customer? |
| **Reliability** | Error rates, retries, idempotent sync failures |
| **Abstention** | Do we correctly choose `NO_ACTION` when evidence is weak? |

---

## Groundedness and unsupported claims

Primary failure mode to catch:

> Model invents evidence.

Evaluation fixtures should include cases where the correct behavior is abstention, and cases where a specific product motion is justified by labeled signals.

---

## Fixtures (planned)

Store labeled examples under `data/evaluation/`:

- input signals + entitlement context
- retrieved document IDs (expected)
- expected structured recommendation or `NO_ACTION`
- known-bad completions with unsupported claims

---

## Relationship to batch

Evaluation runs offline and in CI (planned). It is not a substitute for delta detection — batch still skips LLM calls when signals did not change.

---

## Status

**Planned.** Framework and fixtures are not implemented in this foundation pass.
