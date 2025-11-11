---
name: analyze-work-dir
description: "Analyze working directories"
allowed-tools: Bash(ls:*), Bash(gemini:*), Bash(sort:*), Bash(grep:*), Bash(echo:*), Bash(git:*)
personas: [Code analyzer]
---

# Analyze work directories

Use `gemini` skill

Read file `dir.md`
Do the following depending on the section:

Sections:
- git repos where there are no uncommitted or untracked files
  ignore
- git repos where there are only uncommitted files
  using `gemini` skill analyze repo and add a brief summary of what uncommitted changes mean or intend to do
- git repos where there are only untracked files
  ignore
- git repos where there are both uncommitted and untracked files
  using `gemini` skill analyze repo and add a brief summary of what uncommitted changes mean or intend to do
- directories that don't have git repos as subdirectories and that are NOT git repos
  using `gemini` skill analyze repo and add a brief summary of what this repo is
- empty directories that have nothing in it
  ignore