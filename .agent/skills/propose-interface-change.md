---
skill: propose-interface-change
description: Orchestrates a formal A2A request to modify an API or Data contract outside the agent's ownership.
---

# Skill: Propose Interface Change

## When to use this skill
Use this when you are working on a task (e.g., frontend UI) and realize you need a change in an API endpoint, database schema, or contract that is owned by another agent (e.g., @api-steward or @backend). **DO NOT** modify the file directly if you do not own it.

## Execution Steps

1. **Analyze Requirements:** Determine exactly what data is missing, what type it should be, and why it is necessary for your current task.
2. **Read Template:** Read the `.agent/requests/_change_request_template.toml` file to understand the required structure.
3. **Generate Request:** Create a new TOML file in `.agent/requests/` named `REQ-[YYYYMMDD]-[SHORT_DESC].toml`.
4. **Populate Request:** Fill out the TOML with:
   - `target_owner`: The agent responsible for the change (e.g., `@api-steward`).
   - `task_id`: Your current task ID.
   - `requested_change`: Precise description of the payload or schema change.
   - `impact_scope`: The files you believe will be affected.
5. **Update Team Board:** Update `.agent/team_status.md` to change your status to `🔴 BLOCKED` and mention the request ID you are waiting for.
6. **Stop & Wait:** Halt your execution on the current feature until the target agent processes the request and provides the required artifact.
