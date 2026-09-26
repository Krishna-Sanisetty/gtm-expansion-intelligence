# Batch Pipeline

Daily (or on-demand) orchestration for delta detection, signal derivation,
hierarchy aggregation, AI recommendation, and Salesforce sync.

## Status

**Planned.** `python -m batch.run` prints a placeholder message and does
not connect to Snowflake, Salesforce, or LLM providers.

## Intended flow

1. Query Snowflake for customers/locations changed since last successful run
2. Stop if nothing changed
3. Recalculate deterministic location signals
4. Stop if signal state did not change meaningfully
5. Generate location intelligence where appropriate
6. Aggregate to customer-level signals
7. Invoke AI only when customer signal state changed
8. Validate structured AI response
9. Sync recommendation to Salesforce (Draft)
10. Persist pipeline state

Principle: `No meaningful change → no LLM call → no seller noise.`

## Planned CLI

```bash
python -m batch.run
python -m batch.run --customer CUST-1001
python -m batch.run --dry-run
```
