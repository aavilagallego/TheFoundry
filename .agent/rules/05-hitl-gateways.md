# RULE 05: Human-in-the-Loop (HITL) Gateways

## Objective
Implement "Policy-as-Code" governance. Humans act as strategic auditors, not micro-managers. Agents must not interrupt the user for trivial steps, but MUST halt at critical strategic checkpoints.

## Directives (The 3 Gateways)
You are FORBIDDEN to ask the user for approval on micro-tasks (like writing a single function or running a passing test). You MUST ONLY pause and explicitly request human validation at the following 3 gates:

1. **Planning & Specification Gate (@pm / @architect):**
   - Before any code is written, the functional specification (`docs/spec.md`) MUST be approved by the human user.
2. **Architecture Decision Gate (@architect):**
   - Before implementing any new technology, DB migration, or structural change, the human MUST approve the `ADR` (Architecture Decision Record).
3. **Merge & Deployment Gate (@qa / @devops):**
   - Before code is merged into the `main` branch or deployed to production, the human MUST review the final PR and the QA test report.
