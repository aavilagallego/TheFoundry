# AGENTS.md — [PROJECT_NAME] Constitution

> This file defines persistent rules that ALL agents MUST respect. Violations are defects, not trade-offs. 
> Language is optimized for machine reading (concise, imperative).

---

## 1. Project Identity

| Attribute | Value |
|---|---|
| **Name** | [PROJECT_NAME] |
| **Domain** | [PROJECT_DOMAIN] |
| **MVP Scope** | [MVP_FEATURES_COMMA_SEPARATED] |
| **Code Language** | English (variables, functions, technical comments) |
| **UI Language** | [UI_LANGUAGE] |

## 2. Tech Stack (Immutable without ADR)

| Layer | Technology | Min Version |
|---|---|---|
| Frontend | [FRONTEND_FRAMEWORK_AND_LANG] | [VERSION] |
| Backend | [BACKEND_FRAMEWORK_AND_LANG] | [VERSION] |
| ORM | [ORM_OR_DB_CLIENT] | [VERSION] |
| Database | [DATABASE_TECH] | [VERSION] |
| Auth | [AUTH_PROVIDER] | - |
| Infra | [INFRA_PROVIDER] | - |

> **FORBIDDEN**: Changing tech stack without a formal ADR in `docs/adrs/` approved by @architect.

## 3. Monorepo Structure

```text
[PROJECT_NAME]/
├── AGENTS.md                    ← Project constitution
├── apps/
│   ├── web/                     ← [FRONTEND_APP_DIR]
│   │   └── src/                 
│   │       ├── app/             ← Routing & page layouts
│   │       └── features/        ← Feature-driven modules (e.g. auth, dashboard)
│   └── api/                     ← [BACKEND_APP_DIR]
│       ├── src/                 
│       │   ├── main.py          ← Entrypoint
│       │   └── modules/         ← Domain-driven modules (e.g. auth, database)
│       └── alembic/             ← DB Migrations
├── packages/
│   └── shared/                  ← Shared constants, enums, type definitions
├── docs/                        ← Specs, ADRs, architectural blueprints
├── infra/                       ← IaC, Docker configurations
├── agents/                      ← Agent Cards (A2A capabilities)
├── .agent/
│   ├── rules/                   ← Global behavior rules
│   ├── skills/                  ← Reusable procedures
│   ├── tasks/                   ← Active tasks (A2A physical tickets)
│   ├── requests/                ← Cross-domain change requests (A2A)
│   └── team_status.md           ← Central board for shared awareness
├── evals/                       ← Evaluation criteria
└── runbooks/                    ← Setup, deployment, troubleshooting
```

## 4. Code Conventions

| Context | Convention | Example |
|---|---|---|
| Files/Folders | kebab-case | `[FILE_EXAMPLE].ts` |
| UI Components | PascalCase | `[UI_COMPONENT_EXAMPLE]` |
| Variables/Funcs | camelCase | `[FUNCTION_EXAMPLE]` |
| DB Tables | snake_case plural | `[TABLE_EXAMPLE]` |
| Env Variables | SCREAMING_SNAKE_CASE | `[ENV_EXAMPLE]` |

## 5. Mandatory Patterns

### 5.1 Shared Team Awareness
- ALL agents MUST read `.agent/team_status.md` at the start of their execution to understand what peers are doing.
- ALL agents MUST update `.agent/team_status.md` when they start, pause, or finish a task.

### 5.2 Task Lifecycle & Handoffs
- A task is NEVER implicitly "done". 
- To close a task, an agent MUST:
  1. Verify code compiles/tests pass.
  2. Mark the ticket in `.agent/tasks/` as `[DONE]`.
  3. Create an explicit handoff request in `.agent/requests/` for the next agent (e.g., notifying @qa or @architect).

### 5.3 Step Budgets (Infinite Loop Prevention)
- An agent MUST NOT exceed 5 iterations in a single debugging, testing, or fixing loop.
- If a problem is not solved after 5 attempts, the agent MUST halt, update `.agent/team_status.md` to `🔴 BLOCKED`, document the failure in the task file, and request human intervention.

### 5.4 Context Scoping & Token Economy (MAXIMUM EFFICIENCY)
- **Zero Global Spec Reading**: It is STRICTLY PROHIBITED to read global specification documents (such as `docs/spec.md` or `briefing.md`) for daily tasks. Agents MUST rely exclusively on the localized `.agent-context.md` found in the target module's directory (e.g. `apps/web/src/features/{module}` or `apps/api/src/modules/{module}`).
- **Just-In-Time (JIT) Context Hydration**: The `.agent-context.md` files are generated and updated Just-In-Time (JIT) by `@architect` during epic planning (`plan-epic`) or task assignment (`manage-roadmap`), extracting only the sub-specifications and API contracts relevant to the active tasks from `docs/spec.md`.
- **Precision Searching**: Agents MUST NEVER run recursive grep or searches across the entire workspace. All file searches and directory listings MUST be explicitly scoped to the specific module being edited.
- **Cross-Module Boundaries**: Agents MUST NOT open or read implementation files in another module. If cross-module interaction is needed, read ONLY the target module's `.agent-context.md` to understand its API contract.
- Refer to `.agent/rules/06-context-scoping.md` for the exact mandatory bootstrap procedure.

## 6. Explicit Prohibitions

| # | Prohibition | Reason |
|---|---|---|
| P-1 | NO direct DB access from frontend | Security & Architecture |
| P-2 | NO hardcoded credentials | Security (Use env vars) |
| P-3 | NO unapproved dependencies | Supply Chain Security |
| P-4 | NO `any` in TypeScript | Quality & Predictability |
| P-5 | Context budget limit: 30k tokens | Prevent Context Rot |
| P-6 | NO megaprompts in chat for peers | Use `.agent/requests/` (Pull Model) |
| P-7 | NO destructive DB migrations | Maintain database/data integrity |
| P-8 | NO loading global spec docs or other module files for local tasks | Token optimization & prevention of context rot (Rule 06) |

## 7. Security

- **Least Privilege:** Agents only access paths defined in their `ownership` (AgentCard).
- **Secrets:** Use `.env` files. NEVER commit secrets.
- [ADD_PROJECT_SPECIFIC_SECURITY_RULES]

## 8. Env Variables

```env
# [SECTION_1]
[ENV_VAR_1]=value
```
