---
skill: agent-work-loop
agent: all
trigger: "Any natural language user prompt (e.g. '@agent, check your tasks' or '@agent, create X')"
inputs:
  - "User natural language message"
  - "Current workspace state and active task/request queue"
outputs:
  - "Planning, dependency resolution, autonomous skill execution, and quality control"
---

# Skill: Cognitive Agent Work Loop (Autonomous Workspace Execution)

This skill defines the cognitive state machine that every agent runs upon receiving a prompt, enabling autonomous dependency resolution, task prioritization, and safe architecture escalations.

---

## 🔄 The Work Loop in 6 Phases

### Phase 0: Initialization and Shared Awareness
1. **Kanban Sync:** Read `.agent/team_status.md` to understand the state of the team.
2. **Status Registration:** You MUST update your own status in `.agent/team_status.md` to `🟡 IN_PROGRESS` indicating the current task ID. **Failure to update the Kanban board before executing tasks is a critical violation of framework rules.**

### Phase 1: Intent Detection (Natural Language Intent Parsing)
Parse the user's message semantically to map it to a specific skill or technical workflow:
* *"review tasks / what is pending?"* → Read `.agent/tasks/` and trigger this work loop (`agent-work-loop`).
* *"create endpoint / page / component X"* → Map to the respective code skill (e.g. `create-endpoint.md` or `create-ui-component.md`).
* *"deploy / release"* → Map to deployment skills.
* *"plan epic X / organize sprint Y"* (exclusive to `@architect`) → Run `plan-epic` (which triggers `discover-team`).

---

### Phase 2: Triage, Dependencies, and Prioritization
Scan the workspace to map active tasks and load module-specific context efficiently:
1. **Module Identification:** Map the task to its target sub-directory (e.g., `apps/web/src/features/dashboard`).
2. **Modular Context Loading (Rule 06):**
   * Load only `AGENTS.md` (Global Constitution), `.agent-context.md` from the module folder, and relevant rules.
   * **PROHIBITED:** Reading global specification sheets (`docs/spec.md`, `briefing.md`) or files in other modules unless a dependency contract is declared.
   * Estimate context size. If it exceeds 10,000 tokens, prune context or split tasks.
3. **Queue Ingestion:** Load tasks from `.agent/tasks/{agentId}-tasks.md` and incoming A2A requests from `.agent/requests/{agentId}-requests/`.
4. **Dependency & Blocker Analysis:**
   * Does this ticket require a database schema that is not yet migrated?
   * Does the frontend require an API endpoint not yet released by `@backend`?
   * Are there failures starting local Docker containers, ports, or environments?
   * **Code Dependencies:** If a code dependency is missing, file a formal change request using the `_change_request_template.toml` under `.agent/requests/{targetAgent}-requests/` and apply the *Anti-Deadlock Rule* (proceed with mocks/stubs).
   * **Environment Blockers:** If there are failures with local Docker-compose, system packages, DB setups, or networking, developers are **strictly prohibited** from spending cycles trying to fix it. Create an error ticket in TOML format at `.agent/requests/devops-requests/local-env-blocker.toml` with terminal logs, pause the task, and wait for `@devops` to provide a runbook or fix.
5. **Prioritization:** Sort tasks by:
   * **Blockers:** Tasks that unblock peer agents (highest priority).
   * **Complexity:** Address simpler tasks ("quick wins") first to anchor the base, then work on complex items in isolation.

---

### Phase 3: Architectural Incongruence & Escalation Protocol
Validate specifications against project guidelines before writing code:
* **Multi-tenant Leakage:** Check if database models/tables lack tenant filters (e.g. `tenant_id` or `clinic_id`).
* **Stack Deviations:** Check if tasks introduce unapproved packages or languages outside the stack.
* **Logical Clashes:** Check for contradictions in developer tickets or specifications.
* **MANDATORY ACTION:** **HALT EXECUTION.** Create a revision ticket under `.agent/requests/architect-requests/inconsistency.md` detailing the issue, and notify the user so that `@architect` can resolve the clash.

---

### Phase 4: SDD Planning (Specification-Driven Development)
* Create or update the `implementation_plan.md` in the workspace highlighting files to modify, queries to run, or components to build.
* Create or update `task.md` outlining the checklist for execution.
* Request user "OK" explicitly if the changes are structural or high-impact.

---

### Phase 5: Execution and Tool Utilization
* Map and run the specific procedural skill from `.agent/skills/` for each checklist item.
* **Step Budget (Infinite Loop Prevention):** An agent is **strictly prohibited** from attempting to fix the same bug or test error more than 5 consecutive times. On the 5th failure, the agent must halt, update its status in `.agent/team_status.md` to `🔴 BLOCKED`, document the blocker, and request human intervention.
* Comply with the **Exclusive Ownership Principle** defined in `.agent/rules/concurrency.md`.

---

### Phase 6: Closure and QA Gates
1. **Self-Review:** Run `review-checklist.md` and check evaluation criteria under `evals/`.
2. **Task Closure and Plan Archival:**
   * Mark tasks as `[x]` in `task.md` and archive finished tickets.
   * **Technical Audit Trail:** Save the active `implementation_plan.md` permanently under `docs/architecture/plans/epic-{N}-{agentId}-implementation-plan.md` (where `{N}` is the active Epic and `{agentId}` is the agent ID). This preserves history for debugs and onboarding.
3. **A2A Handoff Notification:** If completing this task unblocks a peer agent, notify them by writing a TOML request under `.agent/requests/{targetAgent}-requests/`.
4. **Pull Next Task:** If all tasks are completed and there are no requests in queue, the agent is **prohibited** from going idle. Write a TOML request file at `.agent/requests/architect-requests/next-task-{agentId}.toml` using the change request template to pull the next task from the roadmap, and notify the user.
5. **Kanban Closure:** Finally, you MUST update your status in `.agent/team_status.md` to `🟢 IDLE` or `🔴 BLOCKED` if waiting for another agent. Leaving your status as `IN_PROGRESS` while inactive breaks the team's shared awareness.
