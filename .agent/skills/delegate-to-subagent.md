---
skill: delegate-to-subagent
description: Formal procedure for creating a task ticket, registering status, and calling the invoke_subagent tool.
---

# Skill: Delegate to Sub-agent

## When to use this skill
Use this when you are a coordinating agent (such as `@pm` or `@architect`) and need a specialized agent (such as `@backend`, `@frontend`, `@api-steward`, or `@qa`) to perform work in their exclusive ownership zone.

## Execution Steps

1. **Verify Requirements:**
   - Ensure that the specifications (`docs/spec.md`) and design docs (ADRs) have been approved by the user (HITL Gates 1 & 2).
   
2. **Create Task Ticket:**
   - Create a new task ticket under `.agent/tasks/{agentId}-tasks/TASK-XXX.md` detailing the exact changes and acceptance criteria.
   
3. **Register Task on Team Status Board:**
   - Update `.agent/team_status.md` to set the target agent's status to `🟡 IN_PROGRESS` and specify the task ID and description.
   
4. **Invoke Sub-agent:**
   - Call the `invoke_subagent` tool with the corresponding parameters:
     - `TypeName`: The name of the agent role (e.g. `self`, `research`, or the specific agent type).
     - `Role`: A 2-5 word description of the subagent's role (e.g., `FastAPI Backend Developer`).
     - `Prompt`: A clear instruction linking to the task file, the code convention rules, and the target module's `.agent-context.md`.
     
5. **Listen for Messages:**
   - Once the subagent is invoked, do not poll or check status in a loop. The messaging system will wake you up when the subagent finishes or requests input.
