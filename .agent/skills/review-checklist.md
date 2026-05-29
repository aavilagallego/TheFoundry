---
skill: review-checklist
agent: qa
trigger: "When a QA review task is assigned or when evaluating a deliverable from a peer agent."
inputs:
  - "Artifact to review (code change, configuration, migration)"
  - "Author agent ID"
outputs:
  - "Pass/Fail report detailing found defects"
---

# Skill: QA Review Checklist

This checklist defines the quality standards that all deliverables must meet before they can be merged.

---

## 1. Universal Checklist (All Artifacts)

### Constitution and Design Spec Compliance
- [ ] Coding conventions respected (naming, folder structures).
- [ ] No hardcoded secrets or credentials (P-2).
- [ ] Code scope strictly matches task/MVP requirements.
- [ ] No unapproved third-party dependencies added (P-3).
- [ ] Imports are clean, ordered, and resolve without errors.

---

## 2. Backend Checklist (`@backend`)

### Architecture and Data Boundaries
- [ ] Queries filter by tenant ID (e.g. `tenant_id` or equivalent) if multi-tenant environment is configured.
- [ ] Database updates/mutations record to audit trails if auditing is required.
- [ ] No N+1 query patterns introduced in database fetches.
- [ ] Database migrations include both up and down/rollback paths.

### Security and API Standards
- [ ] Endpoints pass through authenticated routes/middleware.
- [ ] No database or server stack traces are returned or exposed to the client.
- [ ] API designs use correct HTTP status codes (200, 201, 400, 401, 403, 404, 409).
- [ ] API responses are typed and validated via models/schemas (e.g., Pydantic or equivalent).

---

## 3. Frontend Checklist (`@frontend`)

### Code Quality and Typing
- [ ] Strictly typed with zero use of `any` (P-4).
- [ ] Frontend interface types map accurately to backend API schemas.
- [ ] Modular file layout and imports conform to conventions.

### User Interface and Experience
- [ ] UI texts follow the project's target language.
- [ ] Responsive design verified (layouts do not break on mobile, tablet, or desktop viewports).
- [ ] Asynchronous state handled correctly (displays loading spinners, error banners, and empty states).
- [ ] Visual interaction feedback provided (e.g. disable submit button while loading).

---

## 4. DevOps Checklist (`@devops`)

### Infrastructure and Credentials
- [ ] Secrets retrieved from a secret manager (never stored in plaintext env files).
- [ ] Cloud permissions and service accounts follow the principle of least privilege.
- [ ] Container configurations (Dockerfile, compose) are optimized and secure.

### Monitoring and Safety
- [ ] Health check endpoints defined and configured.
- [ ] Environment validation scripts run and pass successfully.
- [ ] Rollback steps documented and verified.

---

## 5. Report Template

The `@qa` agent must output the review results in the following format:

```markdown
## QA Report — {Artifact Name}
- **Author:** @{agentId}
- **Date:** YYYY-MM-DD
- **Verdict:** ✅ PASS / ❌ FAIL

### Found Defects
| # | Severity | Rule Reference | Description | File Path & Line |
|---|---|---|---|---|
| 1 | High | Concurrency §1 | Unapproved file modification outside write boundary | apps/web/src/features/auth.ts:24 |

### Notes
- [Add any observations, warnings, or recommendation notes]
```
