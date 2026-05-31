# RULE 07: Autonomous Agent Delegation and Sub-agents

## Objective
Prevent role bleed and monologue simulation. Enforce physical division of labor by utilizing background sub-agents instead of inline simulation.

## Directives

1. **Forbidden Inline Simulation**:
   - An agent is STRICTLY PROHIBITED from acting as or simulating another agent in a single chat thread (e.g. saying "I will now act as @backend" or "Switching to @api-steward role").
   
2. **Physical Handoff Delegation**:
   - If a task requires changes in directories owned by another agent, the active agent MUST:
     - Create a formal TOML request file under `.agent/requests/{target_agent}-requests/`.
     - If the active agent has coordinator capabilities (like `@pm` or `@architect`) and has access to system tools, it MUST spawn/invoke the target agent in the background using the `invoke_subagent` tool.
     
3. **Contract and Context Validation**:
   - Before invoking a sub-agent, the parent agent must ensure that the prerequisite contract files (e.g., `.agent-context.md`, shared schemas, API specifications) have been created or updated by `@architect` or `@api-steward` in the workspace.
