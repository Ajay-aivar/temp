---
name: runbook-sop-generator
description: >-
  Generate IT runbook/SOP drafts from incident patterns and KB metadata using
  read-only ServiceNow tools. Use for runbooks, SOPs, troubleshooting guides.
---

# Runbook and SOP Generation

## Workflow

1. Call `search_knowledge_articles(query)` for related KB metadata.
2. Optionally call `list_high_priority_incidents` for repeated patterns.
3. Read `demo_data/Demo_IAM_Configuration_Notes.md` when access/folder topics apply.
4. Produce step-by-step runbook draft.

## Output template

```markdown
# Runbook: [Topic]

## Purpose
[One sentence]

## Pre-checks
1. ...

## Resolution steps
1. ...

## Escalation
...

## Validation
User confirms issue resolved.

---
*Draft — DIT/IAM review required before operational use.*
```

## Safety rules

- Do not invent IAM steps not in demo_data/ or tool output
- Read-only — no ServiceNow changes
