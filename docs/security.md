# Security

Security practices for future implementation. No live credentials belong in this repository.

---

## Secrets

- Use `.env` locally; never commit it (see `.gitignore` and `.env.example`)
- Placeholders only in `.env.example`
- Planned Azure: Key Vault for Snowflake, Salesforce, and LLM credentials
- Rotate keys if accidentally exposed

---

## Authentication (planned)

| System | Approach |
|--------|----------|
| Salesforce | OAuth / connected app; least-privilege integration user |
| Snowflake | Key-pair or SSO-backed service user; role with minimal object access |
| LLM providers | API keys or Azure OpenAI Entra auth via Key Vault references |

---

## Least privilege

- Batch role: read facts, write signal/outcome/state tables only as needed
- Salesforce integration: create/update intelligence objects; Opportunity create only through controlled accept path
- No broad production admin credentials in local configs

---

## PII and customer data

- Synthetic data only in this portfolio project
- Do not commit real customer names, contacts, or case text
- Prefer identifiers over free-text PII in logs

---

## Logging and prompts

- Do not log raw secrets, OAuth tokens, or full credential material
- Treat prompts and retrieved docs as potentially sensitive — avoid shipping real customer content to third parties without policy review in a live deployment
- Redact or hash where practical

---

## Prompt exposure

- Prompt templates are versioned artifacts, not secret keys — but they may contain operational heuristics; review before publishing
- Never embed API keys in prompts or Salesforce fields

---

## Azure (planned)

- Managed identities where possible
- Key Vault references in Container Apps / Jobs
- Monitor / Application Insights with careful PII scrubbing

---

## Status

Foundational ignore rules and env placeholders are in place. Runtime secret management is **planned**.
