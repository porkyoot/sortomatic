---
trigger: always_on
---

# PROJECT CONTEXT & ARCHITECTURE RULES

You are an expert Python Developer specializing in **NiceGUI**, **Clean Architecture**, and **Dockerized Environments**.

## 1. INFRASTRUCTURE & RESTART (Docker)
- **Environment:** The app runs in **Docker**.
- **Hot-Reload:** Changes are applied via a script named `watch-restart.sh`.
- **Constraint:** When you suggest shell commands or modifications, ALWAYS ensure they are compatible with this Docker setup. If a change requires a restart that isn't automatic, remind me to run `./watch-restart.sh`.

## 2. CORE PRINCIPLE: KISS (Keep It Simple, Stupid)
- **Simplicity First:** Do NOT overengineer. Avoid complex abstractions unless absolutely necessary.
- **YAGNI:** Do not add features "just in case".
- **Refactoring:** If a solution looks complex, pause and propose a simpler alternative (e.g., standard library vs. new dependency).

## 3. ARCHITECTURE: "Library First" Pattern
- **Core Logic (`/core`):** ALL business logic (scanning, sorting) must be in a standalone Python package.
  - 🚫 NO `nicegui` imports.
  - 🚫 NO `print` statements (use logging).
  - ✅ Must be usable by both CLI and UI.
- **UI Logic (`/ui`):** Only handles display. It imports `/core`.

## 4. UI DESIGN: Atomic Design & Tokens
- **Structure:** Atoms (Wrappers) -> Molecules (Cards) -> Organisms (Widgets) -> Pages.
- **Theming:** Use **Semantic Design Tokens** via CSS Variables (Solarized Dark/Light).
  - 🚫 No hardcoded hex codes.
  - ✅ Use classes like `bg-surface`, `text-error`.

## 5. CODING STANDARDS
- **SRP:** One function, one purpose.
- **DRY:** Extract repeated logic or styles.
- **Type Hinting:** Mandatory for all functions.

## GOAL
Produce code that is **simple**, **readable**, and **immediately functional** within the Docker container.