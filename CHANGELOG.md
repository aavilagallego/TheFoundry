# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-28

### Added
- **The Foundry Genesis:** Initial release of the Enterprise MAS Bootstrapping Framework.
- **Pull-Based Workflow:** Asynchronous event bus via `.agent/tasks/` and `.agent/requests/`.
- **Kanban Governance:** Mandatory Shared Team Awareness through `team_status.md`.
- **Infinite Loop Protection:** Implemented 5-Step Budgets to prevent token exhaustion and runaway agents.
- **Context Scoping (Rule 06):** Just-In-Time (JIT) context hydration via localized `.agent-context.md` files.
- **A2A TOML Protocol:** Deterministic agent-to-agent communication via `_change_request_template.toml`.
- **Ephemeral Bootstrapper:** Introduction of the `@bootstrapper` Setup Wizard that interviews the user, hydrates `AGENTS.md`, and permanently self-destructs to preserve Least Privilege.
- **Agent Cards:** Pre-configured constraints and ownership boundaries for `@architect`, `@pm`, `@backend`, `@frontend`, `@devops`, `@qa`, `@engineer`, and `@api-steward`.
- **Apache 2.0 License:** Open-sourced for Enterprise adoption.
