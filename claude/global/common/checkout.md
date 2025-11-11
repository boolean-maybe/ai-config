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
- first check if temporary directories exist with: `ls YYYYMMDD*` where `YYYYMMDD` is the current date
- create a new directory under your current directory called `YYYYMMDD-N` where: 
  - YYYY is current year 
  - MM is current month
  - DD is current day
  - N is a number like 1 or 2 etc. Find the smallest number such that a directory does not exist yet

## Checkout projects
`cd` in to this directory and clone git repos with branch `$BRANCH` using command 
`git clone --branch $BRANCH git@git.soma.salesforce.com:commerce-cloud-kernel/$PROJECT.git`

where 
- `$PROJECT` is each project name in $ARGUMENTS
- `$BRANCH` is the branch you are told to check out
if $ARGUMENTS is a single word - it is the name of a single project to work with
if any of the projects in $ARGUMENTS does not exist i.e. git clone fails ask the user if this is a typo and prompt for correct name

### Checkout all

IMPORTANT! USE THIS ONLY if $ARGUMENTS is `all` - otherwise treat $ARGUMENTS as a list of project or a single project name
if $ARGUMENTS is `all` it means - check out all our projects
The list of all projects is retrieved using this command:

```shell
gh repo list commerce-cloud-kernel --topic patching --limit 1000 --json name,url)
```

## cd back into temporary directory
after all is done `cd` into the created `YYYYMMDD` temporary directory and use this as your project directory