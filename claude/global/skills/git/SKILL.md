---
name: git
description: create git commits, git branches, and GitHub pull requests, release and development pull request procedures
allowed-tools: Read, Grep, Glob, Update, "Bash(gh merge origin/master:*)", "Bash(gh pr create:*)"
---

# git and github procedures

read [Version file](~/.claude/common/version-file.md) to understand what a version file and version format is

## Work Item
All work must be assigned a work item in the format `@W-XXX`. Ask user what work item to use
Offer the user a list of work item number/description to choose. Make this list using `getWorkForUsers` tool
Only pull those that are in `In Progress` status
Number work items and allow selecting by number so that the user does not need to type entire work item, for example:
1. W-1234567
2. W-7654321
   and the user can choose to respond with simply 1 or W-1234567

Only work item's name in the form of `W-XXX` is needed. No need to retrieve its details
or description. No need to implement anything in the description

## git commit messages
All commit messages must be prefixed with work item like `@W-XXX commit message`
After `@W-XXX` commit message should include brief description on the same line then empty line then longer description
After `@W-XXX` commit message should start with a lowercase letter
Commit message should only describe the functionality and should not include any "generated with" or "co-authored by" type of text

## github pull requests
All pull request titles and descriptions must be prefixed with work item like `@W-XXX commit message`
The work item selected for the commit should also be used for pull requests
After `@W-XXX` pull request title and descriptions should start with a lowercase letter
Pull request description should only describe the functionality and should not include any "generated with" or "co-authored by" type of text

## Branch Naming
- Branch names should follow `prefix/branch-name` pattern where `prefix` is one of `fix`, `feature`, `release`
- Analyze changes and try to understand if it is a feature or a fix branch if it is a development process
- `branch-name` part is in lowercase using dashes and describes fix or feature. It should not include work item
- Feature branches: `feature/feature-description`
- Bugfix branches: `fix/fix-description`
- Release branches: `release/x.y.z` where x, y, z are numbers (e.g., `release/0.3.0`)
- Main branches: `master` and `develop`

## Building
To verify a build run command appropriate for the repo language
- python: `uv sync && python -m py_compile noreact/*.py`
- java: `./gradlew clean build`

## Development Process
Development process or dev PR is a procedure when the user wants to branch a feature or a fix branch off `develop`
push changes and create a PR to `develop`

1. Assume all changes have been done - no need to check out or pull `develop` branch
2. Run build depending on what language the project is in. Stop here on any error
3. If project has Dockerfile verify docker build
4. Create feature or fix branch from `develop`
5. Add and commit all edited files following commit message guidelines
6. Push to remote
7. Create pull request to `develop` branch following pull request guidelines (`gh pr create --base develop ...`)

## Release Process
Release process or release PR is a procedure when the user wants to create a release branch off `develop`
assign a new version to the project without suffix and create a PR to `master`

1. Run build depending on what language the project is in. Stop here on any error
2. If project has Dockerfile verify docker build
3. Create release branch from `develop`: `release/x.y.z`
4. Check current project version in version file in `origin/master` by using `git fetch origin master && git show origin/master:VERSION-FILE` where VERSION-FILE is version file
5. Update version in version file to be current `origin/master` version incremented by 1. For example, if the current version in version file in `origin/master` is 1.2.3 edit local version file to make it 1.2.4
6. Commit with a commit message `@W-XXX fix version` where `W-XXX` is a work item name
7. Merge `origin/master` into this branch. This will create conflict in version file
8. Resolve conflict in version file in favor of the release branch. Commit with a message `@W-XXX resolve version conflict` where `W-XXX` is a work item name
9. Push to remote branch
10. Create pull request to `master` branch following pull request guidelines

## When complete
When a PR is done:
- print its URL so it can easily be shared
- post in channel C04R5DA87G9 "<@WAWQGMTPA> Vadim Bobrov would like you to review a PR: " and add a URL to PR