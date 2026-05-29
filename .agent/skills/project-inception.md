---
skill: project-inception
agent: bootstrapper
trigger: "Any initial message from the user invoking @bootstrapper to start a new project"
inputs:
  - "User message"
  - "Attached or pasted documents in the chat"
outputs:
  - "Complete monorepo configuration, handoff to @pm, and self-destruction of @bootstrapper"
---

# Skill: Setup Wizard and Self-Destruction (Project Inception)

This skill defines the boot sequence of the **Enterprise MAS Bootstrapping Framework**. The `@bootstrapper` has temporary full access to the repository to inject the DNA of the new project before fading out of existence to guarantee architectural security and the principle of least privilege.

---

## 🚀 Boot Sequence

### Phase 1: Document Ingestion and Discovery
The goal is to perfectly absorb the user's vision.
1. **Read Documents:** If the user attaches a PDF, Markdown, or a long text block with their idea, read the document meticulously.
2. **Gap Analysis:** Extract and deduce the following 4 key variables:
   * **Project Name and Domain**
   * **MVP Scope (Core Features)**
   * **Desired Tech Stack (Frontend, Backend, Database)**
   * **UI Language**
3. **Clarification:** If any critical variable is missing (e.g. the user didn't specify if they prefer Python or Node for the backend), **stop and ask the user**. If the vision is already complete in the document, silently proceed to Phase 2.

---

### Phase 2: Constitution Hydration (`AGENTS.md`)
Replace all template variables (`[PROJECT_NAME]`, `[FRONTEND_FRAMEWORK_AND_LANG]`, etc.) in the `AGENTS.md` file. 
* **Critical Rule:** Ensure you DO NOT delete or modify the governance rules (Gateways, Context Scoping, Step Budgets). You must only inject the technological and business identity into Sections 1, 2, and 3.

---

### Phase 3: Team Scaffolding (Agent Cards)
Based on the Tech Stack defined in Phase 1, configure the physical boundaries of the developers in the `agents/` folder:
* If the Frontend is *Next.js*, ensure `frontend.agent-card.json` has `ownership.write = ["apps/web/"]`.
* If the Backend is *FastAPI* or *Django*, ensure `backend.agent-card.json` has `ownership.write = ["apps/api/"]`.
* Configure `devops.agent-card.json` to manage the deduced infrastructure (e.g. Docker, Vercel, AWS).

---

### Phase 4: Git Reset & Self-Destruct Sequence
This is the final and irrevocable step. To protect the integrity of the project's Least Privilege principle and ensure the user's project is detached from The Foundry template, the `@bootstrapper` must remove all traces of its existence.
1. **Git Disconnect:** Execute the terminal command `git remote remove origin` to disconnect the local repository from The Foundry's GitHub remote.
2. **Delete Files:** Use a terminal command or file tool to **permanently delete** the following files:
   * `agents/bootstrapper.agent-card.json`
   * `.agent/skills/project-inception.md`
   * `start.md`
3. **Final Message:** Issue one final message to the user containing exactly this prompt so they can copy and paste it:
*"Setup completed. The monorepo is secured and disconnected from The Foundry template. You may now run `git remote add origin <your-repo-url>` to link your own repository. Copy and paste the following prompt to start the product definition:"*
`@pm the environment is ready. I want to build a [Insert Project Name]. Please interview me to define the MVP scope, and create the docs/brief.md and docs/roadmap.md.`
