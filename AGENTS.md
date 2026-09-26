# GTM Expansion Intelligence — Agent Instructions

This repository implements `GTM Expansion Intelligence` for the fictional vertical SaaS company `FieldPilot`.

Before making architectural, Salesforce, Snowflake, signal-engine, AI, or data-model changes:

1. Read `docs/project-context.md`.
2. Treat that document as the current source of truth for established architecture and domain decisions.
3. For the FieldPilot Salesforce Account model, treat the **Implemented** fields in `docs/project-context.md` as authoritative. Do not recreate superseded planned names (`Account_Scope__c`, `Branch_Count__c`, `Customer_Segment__c`, `Service_Vertical__c`).
4. Do not silently redesign established concepts.
5. If a task requires changing an established architecture decision, explain the conflict before changing it and update `docs/project-context.md` as part of the same change.
6. Do not fabricate implemented capabilities. Clearly distinguish planned vs implemented functionality.
7. All customers, products, support data, usage metrics, and commercial information in this repository must be synthetic.
8. Never commit credentials, Salesforce authentication data, Snowflake credentials, API keys, access tokens, or real customer data.

Important principles:

- Facts before AI.
- The model can form a hypothesis; it cannot invent evidence.
- Preserve location-level evidence before aggregation.
- Commercial actions happen at the parent business level.
- No meaningful signal change means no LLM call.
- Salesforce is the system of action.
- Snowflake is the system of analysis.
- Human approval is required before commercial opportunity creation.
- Precision matters more than recommendation volume.
- Product recommendations must be entitlement-aware; read the implemented product/entitlement model in `docs/project-context.md` before changing recommendation or Salesforce logic.
