# RULE 03: Task Lifecycle & Completion Loops

## Objective
Ensure agents do not leave tasks hanging. Guarantee deterministic handoffs and clear team awareness.

## Directives
When an agent considers a physical task (located in `.agent/tasks/`) to be completed, it MUST execute the following exact sequence:

1. **Verify Integrity:** Ensure code compiles, types are strict (Rule 01), and tests pass (Rule 02).
2. **Update Task Ticket:** Edit the markdown file in `.agent/tasks/` to change the status from `[IN_PROGRESS]` to `[DONE]`, and add a brief summary of the resolution.
3. **Update Team Board:** Modify `.agent/team_status.md` to set your status to `🟢 IDLE` and clear the current task.
4. **Notify Next Agent (A2A Handoff):** If the workflow requires verification (e.g., QA) or integration, create a TOML request in `.agent/requests/` targeting the next agent (e.g., `@qa` or `@architect`) using the `_change_request_template.toml` structure.
5. **Report to User:** Only after completing steps 1-4, summarize the closure to the human user.
