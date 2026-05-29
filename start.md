# 🚀 The Foundry - Bootstrapping Sequence

**CRITICAL SYSTEM INSTRUCTION FOR THE AI AGENT:** 
You have been invoked to bootstrap this project. You MUST strictly follow the steps below. 
**DO NOT enter "Planning Mode" and DO NOT generate an `implementation_plan.md` artifact.**
Adopt the persona of the `@bootstrapper` agent and act conversationally.
**WARNING: You MUST use your physical tools (file editor, terminal) to execute Step 2 and Step 3. Do not hallucinate the completion of the tasks. Actually modify the files and run the commands.**

---

## Step 1: User Discovery
Ask the user (in a single friendly chat message) for the following details, unless they already provided them:
1. **Project Name & Domain**
2. **MVP Scope** (Core Features)
3. **Preferred Tech Stack** (Frontend, Backend, Database)
4. **UI Language**

*Stop here and wait for the user's response before proceeding to Step 2.*

---

## Step 2: Scaffolding (Execute silently once the user answers)
1. **Hydrate Constitution:** Replace all template variables (like `[PROJECT_NAME]`, `[FRONTEND_FRAMEWORK_AND_LANG]`) in the `AGENTS.md` file with the user's choices. Do not modify any governance rules.
2. **Configure Team Boundaries:** Edit the `agents/*.agent-card.json` files to assign the correct `ownership.write` directories based on the chosen Tech Stack (e.g., `apps/web/` for `@frontend`, `apps/api/` for `@backend`).

---

## Step 3: Git Reset & Self-Destruct
To protect the Principle of Least Privilege and detach from the template:
1. Run `git remote remove origin` in the terminal.
2. **Permanently delete** the following files:
   - `agents/bootstrapper.agent-card.json`
   - `.agent/skills/project-inception.md`
   - `start.md` (this file)
3. Send a final message to the user EXACTLY like this: 
*"Setup completed. The monorepo is secured and detached. Please run `git remote add origin <your-repo>` to link your repository. Then, copy and paste this prompt to start the product definition:"*
`@pm the environment is ready. I want to build a [Insert Project Name]. Please interview me to define the MVP scope, and create the docs/brief.md and docs/roadmap.md.`
