# Claude Code Hooks

This directory contains hook scripts that enhance Claude Code's behavior for this project.

## context-loader.sh

**Purpose**: Automatically loads the right context (backend, frontend, or both) based on your prompt.

**How it works**:
1. Analyzes your prompt for backend/frontend keywords
2. Loads appropriate CLAUDE.md file(s):
   - **Backend keywords** → `backend/CLAUDE.md`
   - **Frontend keywords** → `frontend/CLAUDE.md`
   - **Both detected** → Both files
   - **Neither detected** → Root `CLAUDE.md`

**Examples**:
- "Add a Django endpoint" → Backend context
- "Create a React component" → Frontend context
- "Build user profile feature" → Both contexts
- "Which endpoints do I have" → Root context

**Configuration**: Defined in `.claude/settings.json` under `UserPromptSubmit` hook.

## Adding More Hooks

Create new hook scripts in this directory and register them in `.claude/settings.json`. See [Claude Code documentation](https://docs.anthropic.com/claude/docs/hooks) for details.
