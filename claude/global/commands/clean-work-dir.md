---
name: clean-work-dir
description: "Clean working directories"
allowed-tools: Bash(ls:*), Bash(mkdir:*), Bash(sort:*), Bash(grep:*), Bash(echo:*), Bash(git:*)
personas: [Git repo cloner]
---

# Checkout
go into all subdirectories and for each do the following:

- check if it's a git repo root dir. A git repo root dir is a directory that has .git subdirectory
- also go one level down and check if this is a git repo root dir
- for each git repo root do `git status` and find out if has untracked files or uncommitted changes
- ignore regardless of depth and do not count them as untracked: 
  - `.DS_Store` files
  - `.idea` subdirectories
  - `.specstory` subdirectories
  - `venv` and `.venv` subdirectories
  - `.cursorindexingignore` files
  - `.vscode` subdirectories

For example for subdirectory xxx cd into xxx and check if .git subdir exists to find out if it's a git repo root
If there are directories inside xxx cd into each and check if it's a git repo root
DO NOT go below this level
for each git repo root run `git status`

Then make me a markdown file called dir.md in the following format:

Don't use Markdown tables - only lists

Sections:
- git repos where there are no uncommitted or untracked files
- git repos where there are only uncommitted files
- git repos where there are only untracked files. 
  If there are 4 or less uncommitted files - list each file under repo entry
  If there are 4 or less untracked files - list each file under repo entry
- git repos where there are both uncommitted and untracked files
- directories that don't have git repos as subdirectories and that are NOT git repos
- empty directories that have nothing in it

For each section give its total count

Within each section

list all repos:
- full path from here e.g. subdir/another-subdir
- if a git repo give the name of the repo
- if there are untracked or uncommited files give their counts separately