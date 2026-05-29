# Concurrency and Agent Exclusion Rules

> These rules guarantee maximum parallel development without collisions or rewrites.

## 1. Fundamental Principle: Exclusive Ownership

Every file in the workspace has EXACTLY ONE owner agent. Only the owner may write to that file. Other agents may read it, but MUST NEVER modify it.

## 2. Ownership Map

```text
apps/web/src/features/**  → @frontend (EXCLUSIVE)
apps/web/src/app/**       → @frontend (EXCLUSIVE)
apps/web/Dockerfile       → @devops (EXCLUSIVE)
apps/web/package.json     → @frontend (EXCLUSIVE)
apps/web/*.config.*       → @frontend (EXCLUSIVE)

apps/api/src/modules/**   → @backend (EXCLUSIVE)
apps/api/src/core/**      → @backend (EXCLUSIVE)
apps/api/alembic/**       → @backend (EXCLUSIVE)
apps/api/tests/**         → @backend writes, @qa may append
apps/api/Dockerfile       → @devops (EXCLUSIVE)
apps/api/requirements.txt → @backend (EXCLUSIVE)

packages/shared/types/    → @backend DEFINES, @frontend CONSUMES (read-only)
packages/shared/enums/    → @backend (EXCLUSIVE)
packages/shared/constants/→ @backend (EXCLUSIVE)

infra/**                  → @devops (EXCLUSIVE)
runbooks/**               → @devops (EXCLUSIVE)

docs/**                   → @architect (EXCLUSIVE)
agents/**                 → @architect (EXCLUSIVE)
AGENTS.md                 → @architect (EXCLUSIVE)
.agent/**                 → @architect (EXCLUSIVE)

evals/**                  → @qa (EXCLUSIVE)
```

---

## 3. Change Request (A2A) Protocol

When an agent needs to modify a file or resource outside of its authorized ownership zone:

```text
1. The requesting agent documents:
   - Which file/resource needs changes.
   - The exact proposed modifications.
   - The rationale (context).

2. The owner agent:
   - Evaluates the request.
   - Implements the change (or proposes an alternative).
   - Confirms completion to the requester.

3. The requesting agent:
   - Verifies the changes satisfy the requirement.
   - Continues their work.
```

### Example: `@frontend` needs a new shared type definition

```text
@frontend → @backend:
  "I need to add the 'color' field to the 'ConditionType' interface
   in packages/shared/types/conditions.ts to render condition colors in the UI."

@backend:
  "Done. Added 'color: string' to the shared 'ConditionType'.
   The GET /api/v1/conditions endpoint now returns this field."
```

---

## 4. Git Branches per Agent Role

| Agent | Branch Pattern | Base Branch |
|---|---|---|
| `@frontend` | `feat/web-{feature}` | `main` |
| `@backend` | `feat/api-{feature}` | `main` |
| `@devops` | `infra/{change}` | `main` |
| `@qa` | `qa/{scope}` | `main` |
| `@architect`| `docs/{topic}` | `main` |

### Conflict Resolution Rule
* Every agent works on their dedicated branch.
* Pull requests (PRs) to `main` require a QA review from `@qa`.
* Since branches modify distinct folders, merge conflicts should be minimal. If a conflict occurs, the owner agent of the affected folder resolves it.

---

## 5. Potential Conflict Zones & Mitigation

| Conflict Zone | Risk | Mitigation Strategy |
|---|---|---|
| `packages/shared/` | Concurrent access by `@backend` and `@frontend` | `@backend` is the exclusive writer. `@frontend` has read-only access. |
| `apps/api/tests/` | Concurrent writes by `@backend` and `@qa` | `@backend` writes unit tests; `@qa` writes integration tests in separate files (`test_integration_*.py`). |
| Root configuration files | Miscellaneous system updates | `@devops` is the sole owner of root files (e.g. `.gitignore`, Docker configs). |

---

## 6. Anti-Deadlock Rule

> **No agent should block another while waiting for a deliverable.**
> If an agent is blocked by a pending artifact:
> 1. Use mock data or interfaces (stubs) to proceed.
> 2. Document the dependency in the active task board.
> 3. Continue with the next independent sub-task.
> 4. Integrate when the actual artifact is delivered by the owner.

### Mock/Stub Strategies

| Blocked Agent | Blocked By | Solution |
|---|---|---|
| `@frontend` | Endpoint from `@backend` | Use local mock data satisfying the shared type definition |
| `@backend` | Cloud infrastructure | Use local Docker environment (PostgreSQL/local DB) |
| `@qa` | Code from `@frontend`/`@backend` | Prepare test checklists and plan test cases in advance |
| `@devops` | Requirements from developers | Create boilerplate Dockerfiles and setup shell scripts |

---

## 7. API Contract Communication

To maximize parallelism, `@backend` and `@frontend` MUST agree on contracts BEFORE implementation:

```text
1. @backend defines schemas (e.g., Pydantic) → generates OpenAPI specification.
2. @frontend generates TypeScript types automatically from the OpenAPI spec.
3. Both agents write code concurrently against the agreed contract.
4. During integration, endpoints and API clients are connected.
```

> **Note**: The OpenAPI specification is the source of truth. If it changes, `@backend` must notify `@frontend` BEFORE implementing the change.
