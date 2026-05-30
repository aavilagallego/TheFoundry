---
skill: define-product
agent: pm
trigger: "Any natural language command from the user invoking @pm to define the MVP or project scope."
inputs:
  - "User answers to interview questions"
outputs:
  - "docs/brief.md"
  - "docs/roadmap.md"
  - "docs/spec.md (Functional user stories only)"
---

# Skill: Product Definition and Architect Handoff

This skill defines the standard operating procedure the `@pm` (Product Manager) follows to translate the user's raw idea into actionable product documentation, and then seamlessly hand over the technical design to the `@architect`.

---

## 🔄 Step-by-Step Procedure

### Step 1: Iterative User Interview
* If the user's initial message is vague, ask targeted questions to define the MVP scope, user roles, core features, and non-functional business requirements.
* **CRITICAL:** Do NOT rush the interview. Treat this as a multi-turn, iterative brainstorming session. Bounce ideas back and forth, offer product suggestions, and only proceed to documentation when the user is completely satisfied with the refined concept.
* **CRITICAL:** Do NOT discuss technical implementations (databases, frameworks, deployment). Focus strictly on the "What" and "Why", never the "How".
* **EXECUTION BOUNDARY:** You are a manager, NOT a developer. You MUST NOT write production code or attempt to execute technical tasks yourself under any circumstances.

### Step 2: Documentation Generation
Once the user validates the scope, physically create or update the following documents using your file-editing tools:
1. `docs/brief.md`: Executive summary, target audience, and negative scope (what is NOT included in the MVP).
2. `docs/roadmap.md`: Split the MVP into logical Epics and Sprints.
3. `docs/spec.md`: Write clear, boolean-verifiable User Stories and Acceptance Criteria for the first Epic.

### Step 3: Board Update
* Update `.agent/team_status.md` to change your own status back to `IDLE | Waiting for feedback` and mark `@architect` as `PENDING | Tech Design Required`.

### Step 4: The Architect Handoff
This is the final step of your active loop. You must instruct the user to awaken the `@architect` to begin the technical scaffolding.
* Output a final message to the user EXACTLY like this:

*"Product definition is complete and documented! To proceed with the technical architecture, team sizing, and context scoping, please copy and paste the following prompt:"*

`@architect the product definition is complete. Please read the roadmap, execute the 'plan-epic' skill for the first MVP epic, and establish the technical boundaries for the development team.`
