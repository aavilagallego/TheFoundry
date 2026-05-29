---
skill: generate-adr
description: Standardizes the creation of Architecture Decision Records (ADRs) to document technical choices.
---

# Skill: Generate ADR

## When to use this skill
Use this when you (@architect) need to make a significant technical decision, such as introducing a new technology, changing a core pattern, or altering the database schema radically.

## Execution Steps

1. **Read Template:** Review `docs/adrs/_template.md`.
2. **Assign Number:** Look at the existing files in `docs/adrs/` and determine the next sequential number (e.g., `0001`, `0002`).
3. **Draft Document:** Create a new file `docs/adrs/XXXX-short-title-kebab-case.md`.
4. **Fill Content:**
   - Clearly state the context and the problem.
   - State the decision unambiguously.
   - List the positive and negative consequences. If there are negative consequences, explain the mitigation strategy.
5. **Seek Approval:** Set status to `Proposed` and request human validation. Do NOT mark as `Approved` yourself.
6. **Update Constitution:** If the ADR affects the tech stack or global rules, update `AGENTS.md` once the ADR is approved.
