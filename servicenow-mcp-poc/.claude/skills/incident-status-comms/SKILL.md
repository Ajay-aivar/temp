---
name: incident-status-comms

description:
  Draft stakeholder status communications for open high-priority ServiceNow
  incidents using read-only MCP tools. Use when asked for incident updates,
  outage communications, stakeholder briefings, or status comms for INC numbers.
  
---

# Incident Status Communication Drafting

Pod Charlie Use Case 2 — Wave 1 (Raw / API-assisted).

## When to use

- User asks for a **stakeholder update**, **status communication**, or **incident briefing**
- User provides an incident number (e.g. `INC0007001`)
- User asks for updates on **high-priority** or **critical** open incidents

## Workflow

1. Call **`get_incident_for_status_comms`** if the user gave a specific incident number.
2. Otherwise call **`list_high_priority_incidents`** to find active P1/P2 incidents.
3. Draft the communication using **only** fields returned by the tools.
4. Mark output as **Draft — Incident Manager review required**.

## Output template

Use this structure:

```markdown
**Subject:** Service Update — [short description from incident]

**Current status:** [from state field — e.g. Investigating / In Progress / On Hold]

**Issue:**
[From short_description only]

**Business impact:**
[From impact / business_service if present, else: "Not confirmed from incident data."]

**IT action:**
[From assignment_group and state — e.g. "The [group] team is assigned."]

**Next update:**
A further update will be provided within 30 minutes, or earlier if service is restored.

---
*Draft — pending Incident Manager review. Not sent. No ServiceNow record was modified.*
*Source: ServiceNow read-only MCP — [incident number]*
```

## Safety rules (mandatory)

**Never invent:**
- Root cause
- ETA or fix time
- Resolution confirmation (unless state is Resolved/Closed)
- Names of affected users
- Business impact details not in returned fields

**If data is missing, write exactly:**
`Not confirmed from incident data.`

**Never claim:**
- A message was sent to stakeholders
- A ticket was updated, assigned, resolved, or closed
- Service is restored (unless state confirms it)

## Example trigger phrases

- "Draft status comms for INC0007001"
- "Write a stakeholder update for the payroll server incident"
- "List high-priority incidents and draft status updates"

## Demo incident

`INC0007001` — Employee payroll application server is down (Priority 1, New).
