---
name: incident-post-mortem
description: >-
  Synthesise incident post-mortem drafts from ServiceNow incident data and
  approved resolution notes. Use for post-mortems, RCA drafts, outage reviews.
---

# Incident Post-Mortem Synthesis

## Workflow

1. Call `get_incident_for_post_mortem(INCxxxx)`.
2. Read `demo_data/Demo_INC0007001_Resolution_Notes.md` for timeline/RCA context when needed.
3. Produce structured post-mortem draft.

## Output template

```markdown
# Post-Mortem: [INC number] — [short_description]

## Timeline
[from demo notes or: Not confirmed from incident data]

## Business impact
[from demo notes or: Not confirmed from incident data]

## Root cause
Not confirmed from supplied incident data. [or from approved demo notes only]

## Corrective actions
1. ...

## Lessons learned
...

---
*Draft — Incident Manager / DIT review required.*
```

## Safety rules

- Never invent root cause without approved demo notes
- Do not claim post-mortem was filed in ServiceNow
