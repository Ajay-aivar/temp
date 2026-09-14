---
name: cab-preparation
description: >-
  Draft Change Advisory Board briefs from ServiceNow change_request records
  using read-only MCP tools. Use for CAB prep, change review, risk summaries.
---

# Change Advisory Board Preparation

## Workflow

1. Call `get_change_request_summary(CHGxxxx)` — e.g. `CHG0000024` on the developer instance.
2. If not found, state developer instance may lack sample data.
3. Produce CAB-ready draft.

## Output template

```markdown
# CAB Brief: [CHG number] — [short_description]

## Change summary
[from short_description, category, priority]

## Risk & impact
Risk: [risk field] | Impact: [impact field]

## Implementation plan
[from implementation_plan or: Not confirmed from data]

## Rollback plan
[from backout_plan or: Not confirmed from data]

## Approvals
[from approval field]

---
*Draft — CAB reviewer decision required. No change was executed.*
```

## Safety rules

- Do not claim change was approved or implemented
- Read-only GET only
