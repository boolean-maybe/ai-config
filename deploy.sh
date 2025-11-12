#!/bin/zsh

# Claude Code
cp claude/global/CLAUDE.md ~/.claude/

rm -rf ~/.claude/scripts
cp -R scripts ~/.claude/

rm -rf ~/.claude/commands
cp -R claude/global/commands ~/.claude/

rm -rf ~/.claude/agents
cp -R claude/global/agents ~/.claude/

rm -rf ~/.claude/common
cp -R claude/global/common ~/.claude/

rm -rf ~/.claude/skills
cp -R claude/global/skills ~/.claude/

# THIS DOES NOT GO INTO ~/.claude instead directly in home
cp claude/global/claude.json ~/.claude.json
cp claude/global/statusline.sh ~/.claude/

# NOT COPYING TO NOT OVERWRITE KEYS
#cp claude/global/settings.json ~/.claude/

# Codex

# run like this:
# codex run -f ~/.codex/commands/dev-pr.md

rm -rf ~/.codex/prompts
mkdir ~/.codex/prompts
cp -R claude/global/commands/* ~/.codex/prompts/

rm -rf ~/.codex/config.toml
cp codex/config.toml ~/.codex/


# Opencode

#cp opencode/opencode.json ~/.config/opencode/