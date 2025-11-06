---
name: dev-pr
description: "Create a development PR"
allowed-tools: Bash(gh pr:*), Bash(git add:*), Bash(git merge:*), Bash(git push:*), "mcp__slack__slack_post_message", Update, "Bash(gh merge master:*)"
personas: [Githup PR creator]
---

use "git" skill to create a development PR
if $ARGUMENTS is `feature` create a feature branch if `fix` create a `fix` branch
