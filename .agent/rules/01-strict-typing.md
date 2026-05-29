# RULE 01: Strict Typing Enforcement

## Objective
Prevent silent regressions and ambiguous code generation.

## Directives
1. **NO `any` types allowed:** Under no circumstances should `any` (in TypeScript) or untyped dynamic variables (in Python) be used for production code.
2. **Explicit Return Types:** ALL functions and methods MUST declare an explicit return type.
3. **Data Transfer Objects (DTOs) / Schemas:** All payloads entering or leaving the system MUST be validated using a strict schema (e.g., Zod, Pydantic, OpenAPI).
4. **Validation:** Agents MUST run the local type checker (e.g., `tsc --noEmit` or `mypy`) and ensure 0 errors before marking a code task as complete.
