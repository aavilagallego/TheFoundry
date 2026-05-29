# 🏭 The Foundry: Enterprise MAS Bootstrapping

Welcome to **The Foundry**. 

The Foundry is a **User Friendly - Enterprise Ready** Multi-Agent System (MAS) bootstrapping framework. 

This repository is not just a codebase; it is a **living, autonomous governance environment** designed to orchestrate multiple specialized AI agents (Architect, Backend, Frontend, DevOps, QA, etc.) to build complex software projects entirely from scratch. 

We built The Foundry to solve the most critical failure points of modern AI coding (token amnesia, infinite loops, architectural drift, and agent collisions). It implements a rigorous **"Policy-as-Code"** and **"Pull-Based"** governance model, while remaining completely frictionless for the end-user.

---

## 🌟 Core Philosophy & Architectural Decisions (The "Why")

### 1. Pull-Based Workflow (Coordination as a Dependency)
* **The Problem:** Centralized orchestrator agents pushing tasks to developers often lose context, hallucinate file paths, or spam the chat.
* **The Decision:** We implemented a **Pull Model**. Agents read their own queues in `.agent/tasks/`. If they run out of work, they must file a formal TOML request asking the `@architect` for the next ticket.
* **Why:** This decouples execution from planning, turning the `.agent` directory into a highly resilient, asynchronous Event Bus.

### 2. The Shared Kanban Board (`team_status.md`)
* **The Problem:** Agents work in isolation ("black boxes"). They overwrite each other's code and don't know who is waiting for whom.
* **The Decision:** All agents are constitutionally required to update `.agent/team_status.md` when they start, pause, or finish a task.
* **Why:** This provides **Shared Team Awareness**. If an agent is blocked, human users or peer agents can instantly see the bottleneck on the board.

### 3. Context Scoping & Token Economy
* **The Problem:** Passing a massive `spec.md` to an agent to fix a tiny CSS bug causes "Context Rot", wastes tokens, and confuses the LLM.
* **The Decision:** **Zero Global Spec Reading.** Agents only read a localized `.agent-context.md` file located exactly in the sub-folder they are editing.
* **Why:** This enforces maximum efficiency, keeping the LLM laser-focused on the immediate code boundaries.

### 4. Step Budgets (Infinite Loop Prevention)
* **The Problem:** Agents get trapped in loops trying to fix a failing test, burning thousands of tokens and never succeeding.
* **The Decision:** A strict budget of **5 iterations** per loop. On the 5th failure, the agent MUST halt and update its status to `🔴 BLOCKED`.
* **Why:** Prevents runaway compute costs and forces the system to escalate complex, unresolvable issues to humans or senior agents.

### 5. Deterministic A2A Communication (TOML Protocol)
* **The Problem:** Agents talking to each other using JSON often hallucinate trailing commas or invalid syntax, breaking the pipeline.
* **The Decision:** All Agent-to-Agent (A2A) requests use a strict template at `.agent/requests/_change_request_template.toml`.
* **Why:** TOML is highly fault-tolerant and easily readable by both machines and humans, ensuring zero-error communication.

### 6. The Ephemeral Bootstrapper ("Self-Destructing Setup")
* **The Problem:** Having the Product Manager (`@pm`) modify system configuration files breaks the Principle of Least Privilege.
* **The Decision:** We introduced `@bootstrapper`, an agent that configures the project in a single command and then permanently deletes its own source code.
* **Why:** Provides a magical 1-click onboarding experience while leaving the repository 100% secure and surgically clean for the permanent team.

---

## 📂 Directory Structure & File Definitions

Every file in this repository has a specific purpose. There is no bloat.

### `/AGENTS.md`
**The Constitution.** Immutable rules for all agents. Contains the project domain, tech stack, and explicitly forbidden actions. All agents read this file.

### `/agents/`
Contains the **Agent Cards** (`*.agent-card.json`). These define the personality, constraints, and physical write permissions (ownership) of each agent (e.g. `@frontend`, `@backend`).

### `/.agent/`
The autonomous nervous system of the repository.
* **`rules/`**: Global behavioral logic (e.g. context-scoping, concurrency).
* **`skills/`**: The procedural workflows for agents (e.g. `agent-work-loop.md` for the main loop, `project-inception.md` for the bootstrapper).
* **`tasks/`**: Physical Markdown tickets created by the `@architect` for the developers to pull.
* **`requests/`**: Cross-domain TOML change requests (Agent-to-Agent communication). Includes `_change_request_template.toml`.
* **`team_status.md`**: The real-time Kanban board where agents report their current status.

### `/docs/`
Strategic documentation.
* **`roadmap.md`**: The Master Epic/Sprint plan managed by `@architect`.
* **`brief.md`**: The executive summary of the business vision managed by `@pm`.
* **`adrs/`**: Architecture Decision Records.

### `/evals/`
Automated quality rubrics used by `@qa` to verify code against business requirements before deployment.

---

## 🚀 How to Bootstrap Your Own Project

Anyone can download this framework and use it to build their own software project in a single, frictionless step:

### Step 1: The Magic Prompt
Copy and paste this exact prompt into your AI Agent (Antigravity, Cursor, Claude, etc.):

```text
Clone the repository from https://github.com/aavilagallego/TheFoundry into the workspace.
I want to build a [YOUR PROJECT IDEA]. 
CRITICAL SYSTEM INSTRUCTION: Adopt the persona of the @bootstrapper agent. Do NOT enter Planning Mode and do NOT create an implementation plan artifact. Read the instructions in `.agent/skills/project-inception.md`. Ask me any missing questions (like Tech Stack) conversationally in a single message. Once answered, execute the hydration, handoff, and self-destruct sequence immediately.
```

**The `@bootstrapper` will autonomously:**
1. Clone the repository and interview you to fill any missing gaps (like your preferred Tech Stack).
2. Hydrate the `AGENTS.md` Constitution with your project's DNA.
3. Configure the specific folder boundaries for the `@frontend` and `@backend` agents based on your chosen stack.
4. Draft the initial `docs/roadmap.md` and `docs/brief.md`.
5. Hand over control to the permanent Product Manager (`@pm`).
6. **Self-Destruct:** It will completely remove the Foundry `origin` remote, and permanently delete its own source code to ensure your repository remains perfectly clean.

Once it vanishes, your Enterprise MAS is alive and ready for production.

---

## 📬 Need Help Scaling Your Agents?

Building and managing autonomous AI ecosystems can be challenging. If you need help with your Agent Development, custom workflows, or enterprise implementations, **drop me a line**.

📧 **Contact:** [aavilagallego@gmail.com](mailto:aavilagallego@gmail.com)

---
*Built for the future of autonomous, scalable, and human-aligned AI software engineering.*
