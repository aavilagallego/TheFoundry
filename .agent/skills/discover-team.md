---
skill: discover-team
agent: architect
trigger: "Automatically invoked at the start of any planning or task allocation skill."
inputs:
  - "Agent directory under agents/"
outputs:
  - "Cognitive map of the active squad (IDs, ownership, constraints)"
---

# Skill: Squad Discovery and Role Mapping

This skill defines the autonomous procedure by which the `@architect` discovers the team structure configured in the monorepo. It prevents hardcoding agent roles, adapting dynamically to whatever agent cards exist in the workspace.

---

## 🔍 Discovery Algorithm

### 1. Agent Card Scan
* Read all files matching `agents/*.agent-card.json` in the root of the workspace.
* If any card contains invalid JSON, report an architectural inconsistency.

### 2. Core Metadata Extraction
For each loaded agent card, extract and index in the `@architect` context:
* **Identity:** `agentId` and `displayName` (e.g. `@backend`).
* **Purpose and Role:** Brief description of functional responsibilities.
* **Write Boundaries (Ownership):** Exact folder paths declared under `ownership.write` to know which files the agent controls.
* **Role Constraints:** Rules listed under `constraints` (e.g., "no database access", "no logic modifications") to prevent delegating tasks that violate boundaries.
* **Task Route:** Map the task ticket path: `.agent/tasks/{agentId}-tasks.md`.

---

## 🧠 Cognitive Integration

The generated map must be structured in the `@architect`'s memory as follows before proceeding with planning:

```json
{
  "active_squad": {
    "@backend": {
      "card_path": "agents/backend.agent-card.json",
      "write_zones": ["apps/api/", "packages/shared/"],
      "primary_tasks_file": ".agent/tasks/backend-tasks.md"
    },
    "@frontend": {
      "card_path": "agents/frontend.agent-card.json",
      "write_zones": ["apps/web/", "packages/shared/"],
      "primary_tasks_file": ".agent/tasks/frontend-tasks.md"
    },
    "@devops": {
      "card_path": "agents/devops.agent-card.json",
      "write_zones": ["infra/", "runbooks/"],
      "primary_tasks_file": ".agent/tasks/devops-tasks.md"
    }
  }
}
```

*This dynamic map ensures that any additions or updates to agent cards are immediately recognized by the planning process.*
