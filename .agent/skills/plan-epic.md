---
skill: plan-epic
agent: architect
trigger: "Any natural language command containing 'plan epic X' or 'plan sprint Y' (where X or Y is the ID/Name of the Epic/Sprint)."
inputs:
  - "Project specifications: docs/brief.md, docs/spec.md, docs/roadmap.md, AGENTS.md"
  - "Active team map (result of discover-team)"
outputs:
  - "Physical task tickets created under .agent/tasks/ and notified in chat"
---

# Skill: Epic Planning and Decomposition (Workspace-First)

This skill defines the primary cognitive routine the `@architect` runs when planning a new sprint or roadmap milestone. Its purpose is to decompose an epic into physical, well-structured task tickets, strictly respecting workspace boundaries and avoiding chat megaprompts.

---

## 🔄 Step-by-Step Procedure

### Step 1: Team Discovery and Mapping
* Automatically **invoke the `discover-team` skill** at the start by reading `agents/*.agent-card.json`.
* Register active agents and their allowed write zones to ensure work is delegated within ownership boundaries.

### Step 2: Context and Requirements Grounding
* Read and process repository documentation:
  * `docs/brief.md` (Business objectives and negative scope).
  * `docs/spec.md` (Database models, APIs, and UI designs).
  * `docs/roadmap.md` (Details of active Epics and target Sprints).
* Extract the technical scope belonging to the active Epic/Sprint.

### Step 3: API Contract Validation (@api-steward Handoff)
* If the Epic involves changes to the data models or introduces new API endpoints, you MUST involve the `@api-steward` early in the process.
* Create a request in `.agent/requests/api-steward-requests/` detailing the proposed API changes to ensure OpenAPI contracts are validated before development begins.

### Step 4: Handoff Contract and Dependency Design
* Identify handoff points (e.g., `@backend` must define the OpenAPI schema before `@frontend` can mock or display live data).
* Design the logical task sequence: determine who starts, and apply the *Anti-Deadlock Rule* using mocks for dependencies.
* **EXECUTION BOUNDARY:** You are an Architect, NOT a developer. You MUST NOT write production code or execute the tasks yourself. Your strict job is to dispatch physical tickets to the developer agents.

### Step 5: Just-In-Time (JIT) Context Hydration
* **CRITICAL STEP:** Since developer agents are prohibited from reading global files like `docs/spec.md` to conserve tokens (Rule 06), the `@architect` (or `@pm`) MUST extract the specific specifications for this Epic/Sprint from `docs/spec.md`.
* Dump these specific instructions dynamically into the `.agent-context.md` file in the module folder (e.g., `apps/web/src/features/{module}/.agent-context.md` and `apps/api/src/modules/{module}/.agent-context.md`).
* The JIT context file must contain:
  * Current milestone/MVP phase details.
  * Precise business logic, validation rules, and enums required for the active sprint.
  * API contracts or data models specific to the module's work.

### Step 6: Physical Task Ticket Generation (Workspace-First)
* **GOLDEN RULE:** Do not dump extensive code guidelines or megaprompts in the chat interface.
* Create or overwrite individual task files in `.agent/tasks/{agentId}-tasks.md` for each developer role detected in Step 1.
* **Required Ticket Structure (`.agent/tasks/{agentId}-tasks.md`):**
  1. **Header:** Epic and Sprint name.
  2. **General Info:** Priority, complexity, and active sprint dependencies.
  3. **Task List:** Granular checklist using `[ ]` and `[x]` tasks.
  4. **Acceptance Criteria:** Quality gates mapping to criteria in `evals/`.

### Step 7: Create Cross-Agent Change Requests (A2A)
* If there are immediate blocking dependencies (e.g., Frontend needs Backend's schemas), write a change request under `.agent/requests/{targetAgent}-requests/` to be read during their work loop.

### Step 8: Team Invocation & Chat Notification
* Do NOT ask the user to copy-paste prompts.
* If your platform supports subagent invocation tools (e.g., `invoke_subagent`), launch the `@frontend` and `@backend` agents in the background to execute their physical task tickets.
* If your platform does NOT support background agents, instruct the user to explicitly `@-mention` the developer agents to pass the baton.
* Reply to the user concisely. Confirm that the Epic has been successfully planned, listing the active agents and their assigned tasks (with clickable markdown links).
