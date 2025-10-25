---
name: dev-pr
description: "Create a development PR"
allowed-tools: Bash(gh pr:*), Bash(git add:*), Bash(git merge:*), Bash(git push:*), "mcp__slack__slack_post_message"
personas: [Githup PR creator]
---

# Dev PR

## Work Item
All work must be assigned a work item in the format `@W-XXX`. Ask user what work item to use
Offer the user a list of work item number/description to choose. Make this list using `getWorkForUsers` tool
Only pull those that are in `In Progress` status
Number work items and allow selecting by number so that the user does not need to type entire work item, for example:
1. W-1234567
2. W-7654321
and the user can choose to respond with simply 1 or W-1234567

- All commit messages must be prefixed with work item like `@W-XXX commit message`
- All pull request titles and descriptions must follow the same format

Only work item's name in the form of `W-XXX` is needed. No need to retrieve its details
or description. No need to implement anything in the description

## Version File
The project version is different depending on project language:
- Python - pyproject.toml
- Go - VERSION
- Java gradle.properties

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
1. Run build depending on what language the project is in. For java `./gradlew clean build` and verify it passes. Stop here on any error
2. Create feature or fix branch from `develop`
3. Add and commit all edited files following commit message guidelines
4. Push to remote
5. Create pull request to `develop` branch following pull request guidelines (`gh pr create --base develop ...`)

## When complete
When a PR is done:
- print its URL so it can easily be shared
- post in channel C04R5DA87G9 "<@WAWQGMTPA> Vadim Bobrov would like you to review a PR: " and add a URL to PR

