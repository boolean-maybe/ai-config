---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: make a dev PR to develop branch
---

# Dev PR

## Work Item
All work must be assigned a work item in the format `@W-XXX`. Ask user what work item to use
Offer the user a list of work item number/description to choose. Make this list using `getWorkForUsers` tool
Number work items and allow selecting by number so that the user does not need to type entire work item, for example:
1. W-1234567
2. W-7654321
and the user can choose to respond with simply 1 or W-1234567

- All commit messages must be prefixed with work item like `@W-XXX commit message`
- All pull request titles and descriptions must follow the same format

## Version File
The project version is managed in [gradle.properties](mdc:gradle.properties). This file contains:
- Project version number
- Project group ID
- Dependencies and their versions

## Version Format
- Development versions use the `-SNAPSHOT` suffix (e.g., `0.2.7-SNAPSHOT`)
- Release versions remove the `-SNAPSHOT` suffix (e.g., `0.3.0`)

## Branch Naming
- Branch names should follow `prefix/branch-name` pattern where `prefix` is one of `fix`, `feature`, `release`
- `branch-name` part is in lowercase using dashes and describes fix or feature. It should not include work item      
- Feature branches: `feature/*`
- Bugfix branches: `fix/*`
- Release branches: `release/*` (e.g., `release/0.3.0`)
- Main branches: `master` and `develop`

## Commit Message and Pull Request description
- Commit message should always start with `@W-XXX` where `W-XXX` is work item name. Ask user for this name
- Pull request title and description should follow the same format
- After `@W-XXX` commit message should include brief description on the same line then empty line then longer description
- After `@W-XXX` commit message, pull request title and descriptions should start with a lowercase letter
- Commit message and pull request description should only describe the functionality and should not include any "generated with" or "co-authored by" type of text

## Development Process
1. Run `./gradlew clean build` and verify it passes. Stop here on any error
2. Create feature or fix branch from `develop`
3. Add and commit all edited files following commit message guidelines
4. Push to remote
5. Create pull request to `develop` following pull request guidelines

## When complete
When a PR is done:
- print its URL so it can easily be shared
- post in channel C04R5DA87G9 "<@WAWQGMTPA> Vadim Bobrov would like you to review a PR: " and add a URL to PR

