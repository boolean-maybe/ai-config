---
name: gus
description: create GUS items
allowed-tools: Read, Grep, Glob, Update
---

# GUS procedures
**IMPORTANT: Always use this skill for ANY GUS-related operations including creating work items, looking up work items, updating work items, or commenting on work items. Do NOT use MCP GUS tools directly - always invoke this
skill instead.**

This skill handles all GUS operations including:
- Creating work items (ADM_Work__c)
- Looking up work items by number
- Updating work items
- Adding comments to work items
- Querying work items by user, team, sprint, epic, etc.

When the user mentions work items, GUS, W-numbers, or any related GUS concepts, immediately invoke this skill.

## Create GUS Work Item
Create work item using `createWorkItem` tool
if not specified prompt for subject and optional details and attachments
If no details provided leave emtpy
if no attachments specified do not attach anything
**REQUIRED OUTPUT - DO NOT SKIP:**
- work item number in format W-XXXXXXX (e.g., W-20149403)
- direct URL in format: https://gus.my.salesforce.com/{workItemId}