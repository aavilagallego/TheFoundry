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

## 🤖 Meet the Team: Included Agents & Skills

The Foundry comes pre-configured with a specialized team. Each agent has its own `agent-card.json` dictating its exact permissions and boundaries.

* 🏗️ **`@bootstrapper`**: Ephemeral SysAdmin. Clones, configures, and self-destructs.
* 📊 **`@pm`**: Product Manager. Interviews you to define the MVP, user stories, and writes `brief.md`. Forbidden from touching code.
* 🏛️ **`@architect`**: Enterprise Architect. Designs data models, scopes technical context, and generates physical task tickets for the developers.
* 💻 **`@frontend` & `@backend`**: Software Engineers. They pull their tasks from the Kanban board and write code in their specific folders.
* 🛡️ **`@qa`**: Quality Assurance. Evaluates code against Acceptance Criteria in `evals/`.
* ⚙️ **`@devops`**: Infrastructure Manager. Manages Docker, CI/CD, and deployments.
* 👮 **`@api-steward`**: API Guardian. Ensures OpenAPI contracts are not broken between frontend and backend.

### Key Agent Skills (`.agent/skills/`)
Agents are equipped with physical Markdown "skills" (Standard Operating Procedures):
* **`agent-work-loop.md`**: The core autonomous execution loop every agent follows.
* **`plan-epic.md`**: The Architect's process to decompose business requirements into physical tickets.
* **`manage-context-budget.md`**: Forces agents to strictly manage their token windows.

---

## 💰 FinOps & Token Economy

Running multi-agent systems can get incredibly expensive if agents are allowed to "think globally" on every prompt. The Foundry is engineered for strict FinOps:

* **Just-In-Time (JIT) Context:** Developers are constitutionally forbidden from reading the massive global `docs/spec.md`. The Architect extracts only the tiny pieces they need and creates localized `.agent-context.md` files. This saves millions of input tokens per project.
* **5-Step Execution Budgets:** To prevent agents from getting stuck in infinite debugging loops (which burn tokens exponentially), The Foundry enforces a strict 5-attempt limit. On the 5th failure, the agent must halt and request human intervention.
* **Chat is for Handoffs, not Code:** Instead of pasting thousands of lines of code into the chat UI (which wastes context window), agents write physical tickets and code directly to the file system.

---

## 🚀 How to Bootstrap Your Own Project

Anyone can download this framework and use it to build their own software project in a single, frictionless step:

### Step 1: The Magic Prompt
Copy and paste this exact prompt into your AI Agent (Antigravity, Cursor, Claude, etc.):

```text
Clone https://github.com/aavilagallego/TheFoundry and execute start.md
```

### How It Works: The Domino Effect Workflow
The magic of The Foundry is that you don't orchestrate agents manually; they pass the baton to each other autonomously. When you run the Magic Prompt, you trigger a chain reaction:

1. 🏗️ **Phase 1: Physical Setup (`@bootstrapper`)**
   The AI adopts the SysAdmin persona. It asks for your Tech Stack, configures the repository's rules (`AGENTS.md`), assigns folder permissions, and then **permanently deletes its own source code** for security. Finally, it gives you a prompt to wake up the PM.
   
2. 📊 **Phase 2: Product Definition (`@pm`)**
   The AI switches to the Product Manager persona. It interviews you purely about the business logic to define your MVP scope, creating your `docs/brief.md` and `docs/roadmap.md`. It then gives you a prompt to wake up the Architect.
   
3. 🏛️ **Phase 3: Tech Scaffolding (`@architect`)**
   The Architect takes over. It reads the PM's roadmap, establishes the technical directories, and extracts tiny pieces of context for the developers (to prevent token exhaustion). It generates physical Markdown task tickets.
   
4. 💻 **Phase 4: Isolated Execution (`@frontend` / `@backend`)**
   Your developer agents wake up, read their isolated task tickets from the Kanban board, and start writing code. If they fail a test 5 times, they hit their "Step Budget" and halt to prevent infinite loops.

Once the `@bootstrapper` vanishes in Phase 1, your Enterprise MAS is perfectly governed, alive, and ready for production.

---

## 📬 Need Help Scaling Your Agents?

Building and managing autonomous AI ecosystems can be challenging. If you need help with your Agent Development, custom workflows, or enterprise implementations, **drop me a line**.

📧 **Contact:** [aavilagallego@gmail.com](mailto:aavilagallego@gmail.com)

---
*Built for the future of autonomous, scalable, and human-aligned AI software engineering.*
