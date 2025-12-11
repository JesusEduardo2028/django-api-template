#!/bin/bash

# Claude Code hook: Intelligently loads backend/frontend context based on user prompt
# Analyzes keywords to determine which CLAUDE.md file(s) to inject

set -e

# Get project root directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Define context file paths
BACKEND_CONTEXT="$PROJECT_DIR/backend/CLAUDE.md"
FRONTEND_CONTEXT="$PROJECT_DIR/frontend/CLAUDE.md"
ROOT_CONTEXT="$PROJECT_DIR/CLAUDE.md"

# Backend keywords (Django, API, database, Python)
BACKEND_KEYWORDS=(
    "django" "drf" "rest framework" "api" "endpoint" "serializer" "view" "model"
    "migration" "database" "postgres" "postgresql" "db" "orm" "queryset"
    "pytest" "test_" "factory" "authentication" "token" "permission"
    "settings.py" "urls.py" "admin" "manage.py" "backend/" "core/"
    "python" "pip" "requirements.txt" "gunicorn" "wsgi"
)

# Frontend keywords (React, TypeScript, UI, npm)
FRONTEND_KEYWORDS=(
    "react" "component" "tsx" "typescript" "jsx" "hook" "usestate" "useeffect"
    "frontend/" "src/" "tailwind" "css" "style" "ui" "button" "form" "input"
    "axios" "fetch" "api call" "route" "router" "navigation" "page"
    "npm" "package.json" "node" "jest" "test.tsx" "test.jsx"
    "context" "provider" "authcontext" "interface" "type" "props"
)

# Count keyword matches in the input text
count_matches() {
    local text="$1"
    local keyword_type="$2"
    local count=0
    local lower_text=$(echo "$text" | tr '[:upper:]' '[:lower:]')

    # Use eval to access the array indirectly (Bash 3.2 compatible)
    eval "local keywords=(\"\${${keyword_type}[@]}\")"

    for keyword in "${keywords[@]}"; do
        if echo "$lower_text" | grep -qi "$keyword"; then
            count=$((count + 1))
        fi
    done

    echo "$count"
}

# Read user input from stdin (JSON format from Claude hook)
input_data=$(cat)
prompt=$(echo "$input_data" | jq -r '.prompt // ""')

# Analyze prompt for context relevance
backend_score=$(count_matches "$prompt" BACKEND_KEYWORDS)
frontend_score=$(count_matches "$prompt" FRONTEND_KEYWORDS)

# Determine which context(s) to load
context_content=""

if [ "$backend_score" -gt 0 ] && [ "$frontend_score" -gt 0 ]; then
    # Full-stack query: Load both contexts
    backend_content=$(cat "$BACKEND_CONTEXT" 2>/dev/null || echo "")
    frontend_content=$(cat "$FRONTEND_CONTEXT" 2>/dev/null || echo "")
    context_content="# Backend Context

$backend_content

---

# Frontend Context

$frontend_content"

elif [ "$backend_score" -gt "$frontend_score" ]; then
    # Backend-specific query
    context_content=$(cat "$BACKEND_CONTEXT" 2>/dev/null || echo "")

elif [ "$frontend_score" -gt "$backend_score" ]; then
    # Frontend-specific query
    context_content=$(cat "$FRONTEND_CONTEXT" 2>/dev/null || echo "")

else
    # No specific context detected: Load root context
    context_content=$(cat "$ROOT_CONTEXT" 2>/dev/null || echo "")
fi

# Return JSON output for Claude Code hook
jq -n \
    --arg context "$context_content" \
    '{
        hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: $context
        }
    }'

exit 0
