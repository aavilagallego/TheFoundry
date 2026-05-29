# RULE 06: Context Scoping & Token Economy

## Objective
Minimize LLM context window usage, reduce API latency/cost, prevent "Context Rot" (instruction loss due to large contexts), and guarantee strict API contract coherence.

## Directives

### 1. Strict Context Boundaries
1. **No Global Document Loading**: When executing a task, developer agents MUST NOT load global specification documents (such as `docs/spec.md`, `docs/roadmap.md`, or `briefing.md`) unless the task explicitly requires modifying global architecture.
2. **Context Path Isolation**: Agents MUST restrict their reading of code and documentation files to:
   - The global constitution (`AGENTS.md`).
   - The specific module folder they are working in (e.g. `apps/web/src/features/odontogram/`).
   - The shared packages (`packages/shared/`).
   - The specific task ticket under `.agent/tasks/`.
3. **No Global Workspace Searches**: Running recursive, unrestricted grep or search commands across the entire workspace is strictly prohibited. Searches must always be scoped to the target module directory.

### 2. Bootstrapping Flow
When starting a task, the agent MUST follow this exact sequence to load context:
- **Step A**: Read `AGENTS.md` to load core coding conventions, constraints, and architecture.
- **Step B**: Locate the nearest `.agent-context.md` for the module being modified.
- **Step C**: Load only the specific files inside that module folder needed for the edit.

### 3. API Coherence & Cross-Module Dependencies
1. **Contract First**: Any changes that alter routes, models, or schemas MUST be verified against `packages/shared/` to ensure frontend-backend type safety.
2. **No Cross-Module Reading**: If a module depends on another, the agent is allowed to read only the target module's `.agent-context.md` file. Reading the full implementation files of other modules is prohibited.
3. **Change Requests for API modification**: If a backend API change is required to support a frontend feature, the frontend agent MUST NOT modify or read the backend module files directly. It must create an A2A change request targeting `@backend` in `.agent/requests/` and use mock contracts in the meantime.

### 4. Context Budget Gate
Before submitting a prompt, the agent must estimate the context size of the loaded files. If it exceeds **10,000 tokens** (approx. 35 KB of Markdown/Code), the agent MUST halt execution, prune unnecessary files from its context, or ask the user to break down the task into smaller sub-tasks.

### 5. Just-In-Time (JIT) Context Hydration
1. **JIT Lifecycle**: The `.agent-context.md` files in each module directory are generated and updated Just-In-Time (JIT) by the `@architect` at the start of each Epic or Sprint, and updated during pull-based task allocation.
2. **Derivation from Global Specs**: The `@architect` extracts only the relevant specifications, API schemas, and business rules from the global `docs/spec.md` and dumps them into the module's `.agent-context.md`.
3. **No Stale Contexts**: Developers MUST treat `.agent-context.md` as volatile JIT assets. If they find outdated information, they must request `@architect` to regenerate the context file rather than referring to global files.

