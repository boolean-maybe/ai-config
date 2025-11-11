---
name: checkout
description: "Get master versions"
allowed-tools: Bash(ls:*), Bash(mkdir:*), Bash(sort:*), Bash(grep:*), Bash(echo:*), Bash(git:*)
personas: [Git repo cloner]
---

# Checkout

use [Checkout](~/.claude/common/checkout.md) to check out every project in $ARGUMENTS with branch `master`

read [Version file](~/.claude/common/version-file.md) to understand what a version file is


## Check version
For each project check current project version in version file
For each project print its name and current version
if any of the projects in $ARGUMENTS does not exist i.e. git clone fails ask the user if this is a typo and prompt for correct name

## cd back into temporary directory
after all is done `cd` into the created `YYYYMMDD` temporary directory
delete all checked out projects