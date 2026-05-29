---
skill: manage-context-budget
agent: all
trigger: "When generating documentation, editing skills, evals, or global constitution rules."
inputs:
  - "The set of Markdown files composing the agent's active context"
outputs:
  - "Context token report and refactoring/compaction plan if limits are exceeded"
---

# Skill: Context Budget and Token Control (FinOps)

## Context Audit Procedure

To prevent LLM context saturation, reduce API latency, and optimize token costs, run this analysis whenever creating or modifying project documentation or rule files (`AGENTS.md`, `docs/`, `evals/`, `.agent/`).

### 1. Identify the Role Context
Calculate the size of only the Markdown files that your agent role reads at startup:
* **Core Global (All Agents):** `AGENTS.md`, `.agent/rules/06-context-scoping.md`, `.agent/rules/concurrency.md`
* **Core Local (Active Module):** `.agent-context.md` (e.g., `apps/web/src/features/{module}/.agent-context.md` or `apps/api/src/modules/{module}/.agent-context.md`)
* **Backend Agent:** `evals/backend-criteria.md` and related backend skills.
* **Frontend Agent:** `evals/frontend-criteria.md` and related frontend skills.

> [!WARNING]
> Loading large global specification files (like `docs/spec.md` or `briefing.md`) by default is strictly prohibited. Rely on the Just-In-Time (JIT) context updated by `@architect` in `.agent-context.md`.

### 2. Measure Context Size (PowerShell on Windows)
Run this command in the terminal to measure the total size of active Markdown files:

```powershell
Get-ChildItem -Path . -Recurse -Filter *.md | Measure-Object -Property Length -Sum
```

#### Token Estimation Formula (English/Code Mix):
$$\text{Estimated Tokens} = \frac{\text{Total Bytes (Sum)}}{3.5}$$

### 3. Evaluate Budget Thresholds

#### Global Constitution & Governance Budget (Sum of AGENTS.md + active global docs)
| Token Range | Status | Required Action |
|---|---|---|
| **< 20,000 tokens** | **GREEN (Safe)** | Proceed as normal. |
| **20,000 - 25,000 tokens** | **YELLOW (Warning)** | Avoid redundant wording. Add critical points in a concise list format only. |
| **> 25,000 tokens** | **RED (Blocked)** | **STOP.** No additional documentation can be added until global context files are pruned or refactored. |

#### Local Module Context Budget (Individual `.agent-context.md` file)
| Token Range | Status | Required Action |
|---|---|---|
| **< 4,000 tokens** | **GREEN (Safe)** | Proceed as normal. |
| **4,000 - 5,000 tokens** | **YELLOW (Warning)** | Compact the file. Remove code stubs or narrative prose. |
| **> 5,000 tokens** | **RED (Blocked)** | **STOP.** Refactor the local file by splitting specifications or moving details into code docstrings. |

---

## Markdown Compression and Compaction Techniques

If your context enters the **RED status**, apply these compaction methods to clean the files:

### A. Replace Prose with Compact Checklists
* **Before (Verbose):**
  > "To implement this component, the developer will need to verify carefully that the layout is responsive on all viewports. This means that both on mobile phones around 360px wide and on high-resolution desktops up to 1920px, the navigation bar should not overlap or wrap incorrectly."
* **After (Compressed - Saves 75% tokens):**
  > "* Responsive layout: functional from 360px to 1920px without overlaps."

### B. Consolidate Duplicate Skills
If multiple skills overlap (e.g., `create-page.md` and `create-dialog.md`), consolidate them into a single generic skill (e.g., `create-ui-component.md`) and remove extensive code samples that can be found in reference code.

### C. Minimize Example Code Blocks
Code blocks inside Markdown rules must remain conceptual and short (maximum 15 lines). Never include production code stubs in `.md` rules.
