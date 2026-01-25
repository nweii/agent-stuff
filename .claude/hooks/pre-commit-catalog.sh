#!/bin/bash
# ABOUTME: Pre-commit hook that updates catalog when skills/commands change
# ABOUTME: Runs update-catalog.py and stages README.md if skills or commands are modified

set -e

# Parse hook input JSON
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))")
COMMAND=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('command', ''))")

# Only proceed for Bash tool with git commit commands
if [ "$TOOL_NAME" != "Bash" ] || [[ ! "$COMMAND" =~ git\ commit ]]; then
    exit 0
fi

# Change to agent-stuff directory
cd "$CLAUDE_PROJECT_DIR" || exit 1

# Check if any staged files are in skills/ or commands/
STAGED_SKILLS=$(git diff --cached --name-only | grep -E '^(skills|commands)/' || true)

if [ -z "$STAGED_SKILLS" ]; then
    # No skills/commands changed, nothing to do
    exit 0
fi

# Skills or commands changed, update catalog
echo "Skill/command files changed, updating catalog..." >&2

python3 scripts/update-catalog.py

# Check if README.md was modified
if git diff --name-only README.md | grep -q README.md; then
    # README changed, stage it
    git add README.md
    echo "Catalog updated and staged README.md" >&2

    # Provide context to Claude via stdout
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "Auto-updated skills catalog in README.md before commit (skills/commands were modified)"
  }
}
EOF
else
    echo "Catalog already up to date" >&2
fi

exit 0
