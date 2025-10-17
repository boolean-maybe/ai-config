---
name: dev-pr
description: "Create a development PR"
allowed-tools: Bash(git add:*), Bash(git push:*)
personas: [Githup PR creator]
---

# Make a release

## Work Item
All work must be assigned a work item in the format `@W-XXX`. Ask user what work item to use
Offer the user a list of work item number/description to choose. Make this list using `getWorkForUsers` tool
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

## Release Process
1. Run build depending on what language the project is in. For java `./gradlew clean build` and verify it passes. Stop here on any error
2. Create release branch from `develop`: `release/x.y.z`
3. Check current project version in version file in `origin/master` by using `git fetch origin master && git show origin/master:VERSION-FILE` where VERSION-FILE is version file
4. Update version in version file to be current `origin/master` version incremented by 1. For example, if the current version in version file in `origin/master` is 1.2.3 edit local version file to make it 1.2.4
5. Commit with a commit message `@W-XXX fix version` where `W-XXX` is a work item name
6. Merge `master` into this branch. This will create conflict in version file
7. Resolve conflict in version file in favor of the release branch. Commit with a message `@W-XXX resolve version conflict` where `W-XXX` is a work item name
8. Push to remote branch
9. Create pull request to `master` branch following pull request guidelines

## When complete
When a PR is done:
- print its URL so it can easily be shared
- post in channel C04R5DA87G9 "<@WAWQGMTPA> Vadim Bobrov would like you to review a PR: " and add a URL to PR

