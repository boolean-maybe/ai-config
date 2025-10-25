---
name: checkout
description: "Checkout projects"
allowed-tools: Bash(ls:*), Bash(mkdir:*), Bash(sort:*), Bash(grep:*), Bash(echo:*), Bash(git:*)
personas: [Git repo cloner]
---

# Checkout

## Do not use &&
Do not use `&&` in your bash commands
For example if you need to execute `cd dir && ls -l` execute `cd` and `ls -l` as separate bash commands

## Creating temporary directory
- first check if temporary directories exist with: `ls 20251023*`
- create a new directory under your current directory called `YYYYMMDD-N` where: 
  - YYYY is current year 
  - MM is current month
  - DD is current day
  - N is a number like 1 or 2 etc. Find the smallest number such that a directory does not exist yet

## Checkout projects
`cd` in to this directory and clone git repos with branch `develop` using command 
`git clone --branch develop git@git.soma.salesforce.com:commerce-cloud-kernel/$PROJECT.git` 
where `$PROJECT` is each project name in $ARGUMENTS
if any of the projects in $ARGUMENTS does not exist i.e. git clone fails ask the user if this is a typo and prompt for correct name

## cd back into temporary directory
after all is done `cd` into the created `YYYYMMDD` temporary directory and use this as your project directory

