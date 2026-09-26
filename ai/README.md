# AI Layer

Interprets verified signals, retrieves product knowledge, forms hypotheses,
and produces structured seller recommendations.

## Status

**Planned.** No LLM calls, prompts, or retrieval indexes are implemented.

## Role

- Interpret verified account/location signals
- Retrieve fictional product documentation (RAG)
- Form hypotheses and explain recommendations
- Generate discovery questions and talk tracks
- Abstain (`NO_ACTION`) when evidence is weak

The AI must not invent operational facts.

> The model can form a hypothesis. It cannot invent the evidence.

## Layout (planned)

| Path | Purpose |
|------|---------|
| `orchestration/` | Recommendation workflow |
| `prompts/` | Versioned prompt templates |
| `retrieval/` | RAG / embeddings over product docs |
| `tools/` | Constrained tools the model may call |
| `schemas/` | Structured output contracts |
| `evaluation/` | Offline quality evaluation |
