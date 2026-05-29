# RULE 02: Test-Driven Guardrails

## Objective
Act as an automated firewall. AI agents cannot send broken implementations to human supervisors or other agents.

## Directives
1. **Mandatory Test Execution:** Agents MUST run the validation scripts (e.g., `npm test`, `pytest`) before proposing any code diffs or PRs.
2. **Green State Requirement:** The environment state MUST return a successful response (Green) before the task is considered done.
3. **Self-Healing Loop:** If a test fails, the agent MUST read the test output, fix the code, and re-run the test. Do not request human intervention for a failing test unless stuck in a loop of more than 3 attempts.
4. **Test Coverage:** New features MUST include basic unit tests covering the happy path and at least one edge case.
