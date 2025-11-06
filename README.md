# cursor-rules
Cursor rules both user and project

# Claude
https://docs.anthropic.com/en/docs/claude-code/iam
https://github.com/ericbuess/claude-code-docs/blob/main/docs/model-config.md
https://github.com/Njengah/claude-code-cheat-sheet/

run with haiku 4.5:
```shell
export ANTHROPIC_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
claude
# or
claude --model us.anthropic.claude-haiku-4-5-20251001-v1:0
# or
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
claude --model haiku
```

get available models:
```shell
curl -X GET "https://eng-ai-model-gateway.sfproxy.devx-preprod.aws-esvc1-useast2.aws.sfdc.cl/v1/models" --header "Authorization: Bearer TOKEN"
```

```shell
# Add additional working directories
claude --add-dir ../apps ../lib
```

```shell
claude --dangerously-skip-permissions
```
## claude.json vs settings.json

There is a significant amount of discussion among developers about the differences and confusion between Claude Code’s `~/.claude.json` (sometimes seen as `.claude.json`) and `~/.claude/settings.json` configuration files. Both have distinct purposes, but their overlapping roles and the way Claude Code handles configuration priorities can create practical headaches for users[1][2][3].

### Purpose and Hierarchy

- **`~/.claude.json` ("Legacy" or Main Global Config)**
    - This file is often described as an unofficial or legacy configuration location[1]. Some users report it as the only place where certain global settings or mixed project configurations will “actually work,” especially for things like MCP server definitions, prompt and usage history, and miscellaneous stats[1][3][4].
    - The structure can become messy and is less predictable, but it is referenced by the tool when user or project-specific configs don’t apply or aren’t found[1][2].
    - This file typically has the highest priority when present, but is not considered best practice for modern usage[2].

- **`~/.claude/settings.json` (User-Specific Global Settings)**
    - This is the current, documented location for personal configuration settings that should apply globally to your user account across all projects[1][5][6][7].
    - Typical settings include your preferred model, UI/theme options, API keys, tool enable/disable toggles, and any default behaviors you want to set for all projects[1].
    - Considered cleaner, more maintainable, and intended for user defaults[2].

### Common Issues and Interactions

- The interactions between these files—and with project/local configs—are a frequent source of confusion. The Claude Code config hierarchy looks like:
    1. `~/.claude.json` (legacy, highest priority, fallback for odd issues)
    2. `~/.claude/settings.json` (user global config)
    3. `.claude/settings.json` (per-project settings, often checked into source control)
    4. `.claude/settings.local.json` (personal tweaks for individual projects, not in source control)[1][2]
- Settings in one file can unexpectedly be overridden by another, making it difficult to debug problems or reliably set global options[1].

### Community Comments

- Reddit and GitHub issue discussions indicate that many users wind up editing both files, especially when something doesn’t “stick” in the documented settings location[8][3].
- The `.claude.json` file is especially problematic for teams or automation, as it can mix personal and project settings and is not recommended for sharing[1][3].

### Best Practice

- For new installations or teams: favor `~/.claude/settings.json` for user defaults, and `.claude/settings.json` inside a project for settings meant to be shared.
- Use `~/.claude.json` only for legacy compatibility or as a last resort if something isn’t working as expected in the supported files[1][2][3].

In summary, `~/.claude/settings.json` is the clean, user-facing configuration file, while `~/.claude.json` is a messy legacy file that persists for backward compatibility and edge cases. The distinction and inheritance order can trip up even advanced users, so careful management and awareness of overrides are recommended[1][2][3].

Sources
[1] A developer's guide to settings.json in Claude Code (2025) - eesel AI https://www.eesel.ai/blog/settings-json-claude-code
[2] Where Are Claude Code Global Settings Files Located - ClaudeLog https://www.claudelog.com/faqs/where-are-claude-code-global-settings/
[3] settings.json location · Issue #1202 · anthropics/claude-code - GitHub https://github.com/anthropics/claude-code/issues/1202
[4] Configuring MCP Tools in Claude Code - The Better Way https://scottspence.com/posts/configuring-mcp-tools-in-claude-code
[5] Claude Code settings https://docs.claude.com/en/docs/claude-code/settings
[6] Claude Code - Truefoundry Docs https://docs.truefoundry.com/gateway/claude-code
[7] Claude Code - Z.AI DEVELOPER DOCUMENT https://docs.z.ai/scenario-example/develop-tools/claude
[8] Claude Code settings.json : r/ClaudeAI - Reddit https://www.reddit.com/r/ClaudeAI/comments/1l24a93/claude_code_settingsjson/
[9] Extend Environment Variable Expansion to `settings.json` files ... https://github.com/anthropics/claude-code/issues/4276
[10] Claude's "Secret" JSON Mode Explained - YouTube https://www.youtube.com/watch?v=U7uVeHf7TFs
[12] MCP Configuration Inconsistency: CLI-managed vs File-based configs https://github.com/anthropics/claude-code/issues/3098
[13] Claude Code Configuration Guide | ClaudeLog https://www.claudelog.com/configuration/
[14] How I use Claude Code (+ my best tips) - Builder.io https://www.builder.io/blog/claude-code
[15] Claude Code: Best practices for agentic coding - Anthropic https://www.anthropic.com/engineering/claude-code-best-practices
[16] Configuring Claude Code | AI Native Dev https://ainativedev.io/news/configuring-claude-code