---
name: clean-work-dir
description: "Clean working directories"
allowed-tools: Bash(ls:*), Bash(python3 /Users/vbobrov/.claude/skills/cleaner/analyze_repos.py:*), Bash(sort:*), Bash(grep:*), Bash(echo:*), Bash(git:*)
personas: [Code analyzer]
---

# Analyze work directories

use [repo analyzer script](../../../scripts/analyze_repos.py) to generate markdown file:
```shell
python3 ~/.claude/scripts/analyze_repos.py
```

Read file `dir.md`
Do the following depending on the section:

USE skill passed in $ARGUMENTS!
if $ARGUMENTS is empty - prompt user for the skill name

Sections:
- git repos where there are no uncommitted or untracked files
  ignore
- git repos where there are only uncommitted files
  using $ARGUMENTS skill analyze repo and add a brief summary of what uncommitted changes mean or intend to do to its `dir.md` entry
- git repos where there are only untracked files
  ignore
- git repos where there are both uncommitted and untracked files
  using $ARGUMENTS skill analyze repo and add a brief summary of what uncommitted changes mean or intend to do to its `dir.md` entry
- directories that don't have git repos as subdirectories and that are NOT git repos
  using $ARGUMENTS skill analyze repo and add a brief summary of what this repo is to its `dir.md` entry
- empty directories that have nothing in it
  ignore