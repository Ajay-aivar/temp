---
name: kb-article-from-ticket
description: >-
  Draft Knowledge Base articles from resolved ServiceNow incidents using
  read-only MCP tools. Use when asked for KB drafts, knowledge articles,
  or documentation from closed tickets.
---

# KB Article Drafting from Resolved Tickets

## Workflow

1. Call `get_resolved_incidents` or `get_incident_for_kb_draft(INCxxxx)`.
2. If close_notes are empty or generic, read `demo_data/Demo_INC0000013_Resolution_Notes.md` when relevant.
3. Draft KB article using only returned data + approved demo notes.
4. Mark as **Draft — IT SME review required before publishing**.

## Output template

```markdown
# [Title from short_description]

## Symptoms
[from short_description]

## Likely cause
[from close_notes if usable, else: Not confirmed from incident data]

## Resolution steps
[numbered steps from close_notes or demo file only]

## Escalation
[to assignment_group or standard escalation text]

---
*Draft — IT SME review required. Not published. Source: [INC number]*
```

## Safety rules

- Do not invent steps not in close_notes or demo_data/
- Do not claim article was published to ServiceNow KB
