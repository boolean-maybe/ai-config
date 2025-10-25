#!/bin/zsh

# Claude Code
rm -rf ~/.claude/commands
cp -R claude/global/commands ~/.claude/

rm -rf ~/.claude/agents
cp -R claude/global/agents ~/.claude/
cp -R claude/global/skills/* ~/.claude/skills/

cp claude/global/claude.json ~/.claude/
#cp claude/global/settings.json ~/.claude/

# Codex

# run like this:
# codex run -f ~/.codex/commands/dev-pr.md

rm -rf ~/.codex/prompts
mkdir ~/.codex/prompts
cp -R claude/global/commands/* ~/.codex/prompts/

rm -rf ~/.codex/config.toml
cp codex/config.toml ~/.codex/
