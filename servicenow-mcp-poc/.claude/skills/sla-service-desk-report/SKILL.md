---
name: sla-service-desk-report
description: >-
  Create weekly service-desk and SLA narrative reports from open ServiceNow
  incident aggregates. Use for SLA reports, weekly IT ops summaries, backlog reviews.
---

# SLA and Service-Desk Reporting

## Workflow

1. Call `get_open_incident_category_summary(limit=25)`.
2. Optionally call `list_high_priority_incidents` for critical items.
3. Produce executive-friendly weekly narrative.

## Output template

```markdown
# Weekly Service Desk Summary

**Total incidents reviewed:** [from tool]
**Open incidents:** [count]
**High/Critical:** [from priority breakdown]

## By category
[table or bullets from incidents_by_category]

## By assignment group
[from incidents_by_assignment_group]

## Key findings
[only from returned data]

## SLA note
If made_sla blank: SLA breach status not confirmed from supplied data.

---
*Draft — DIT manager validation required.*
```

## Safety rules

- Do not fabricate SLA breach counts
- Counts reflect tool limit only — state this clearly
