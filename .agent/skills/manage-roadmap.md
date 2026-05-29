---
skill: manage-roadmap
agent: architect
trigger: "When a developer agent requests their next ticket due to lack of tasks (via next-task JSON in .agent/requests/architect-requests/)"
inputs:
  - "JSON request file from the requesting agent"
  - "Master roadmap at docs/roadmap.md"
outputs:
  - "New task ticket assigned in .agent/tasks/ and request queue cleaned"
---

# Skill: Strategic Roadmap Management and Pull-based Task Allocation

This skill defines the standard operating procedure the `@architect` follows to orchestrate task allocation under the Pull Model ("Coordination as a Dependency").

---

## 🔄 4-Step Assignment Procedure

### 1. Request Scan and Ingestion
Whenever invoked by the user or when checking task workflows:
* Scan `.agent/requests/architect-requests/` for files matching `next-task-{agentId}.json`.
* Read the agent ID and the completed task log.

---

### 2. Status and Dependency Validation
Before assigning a new roadmap ticket, verify task constraints in `docs/roadmap.md`:
* Does the upcoming ticket for this agent require a prior release from another agent?
  * *Example:* The `@frontend` agent cannot integrate the live API if the `@backend` agent hasn't generated the OpenAPI specification yet.
* *Decision Rule:* If a block exists, apply the **Strict Dependency Rule**: assign an alternative lower-priority task without blocks, or instruct the agent to build against mocks.

---

### 3. Task Ticket Generation and JIT Local Context Hydration
* Consult `docs/roadmap.md` to identify the active Epic and Sprint.
* **CRITICAL CONTEXT STEP:** Extract from `docs/spec.md` (or other global docs) only the technical specifications relevant to this ticket (e.g. enums, API models, UI behaviors). Write this information into the target module's `.agent-context.md` file. This populates a "Just-In-Time Context" for the developer agent, saving significant input tokens.
* Write a new task file (or update the active list) at `.agent/tasks/{agentId}-tasks.md`.
* **Ticket Structure:**
  * **Ticket Name:** Aligned with the Epic.
  * **Priority and Impact:** Mark if the change is structural (requires review).
  * **Sub-tasks:** Detail deliverables with `[ ]` checkboxes.
  * **Acceptance Criteria:** Link to criteria in `evals/`.

---

### 4. Cleanup and Ingestion Queue Resolution
* Move the handled JSON request from `.agent/requests/architect-requests/next-task-{agentId}.json` to `.agent/requests/architect-requests/archive/` to keep the workspace clean.
* Notify the user and the requesting agent in the chat that their task file has been updated.
