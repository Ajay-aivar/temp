# ServiceNow DIT Use Cases — Simple Guide

This guide explains all **6 Pod Charlie use cases** in plain language: what problem each one solves, when to use it, what you type, and what you get back.

Everything is **read-only**. Claude pulls data from ServiceNow, writes a **draft**, and a human (IT/DIT manager) reviews before anything is sent or published.

```text
You ask Claude → MCP tool reads ServiceNow → Skill formats a draft → Human reviews
```

---

## Quick reference


| #   | Use case                     | When you need it                                                    | Example prompt                                      | Demo ID    |
| --- | ---------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- | ---------- |
| 1   | KB Article Drafting          | Same fix keeps coming up — turn a closed ticket into a KB article   | `Draft a KB article from INC0000013`                | INC0000013 |
| 2   | Incident Status Comms        | Outage or P1/P2 — tell stakeholders what's happening                | `Draft status comms for INC0007001`                 | INC0007001 |
| 3   | Post-Mortem Synthesis        | Major incident is over — document what happened and what to improve | `Draft post-mortem for INC0007001 using demo notes` | INC0007001 |
| 4   | Runbook / SOP Generation     | Team needs step-by-step instructions for recurring issues           | `Create a runbook for shared folder access issues`  | —          |
| 5   | SLA & Service-Desk Reporting | Weekly ops review — how is the backlog looking?                     | `Weekly service desk summary from open incidents`   | —          |
| 6   | CAB Preparation              | Change going to CAB — need a brief for reviewers                    | `Prepare CAB brief for CHG0000024`                  | CHG0000024 |


---



## Use Case 1 — KB Article Drafting from Resolved Tickets



### The problem

Your team fixes the same issue again and again (e.g. slow email with attachments), but the solution lives only in one closed ticket. New engineers don't know the fix. Writing a Knowledge Base article takes time.

### Where it fits

- After an incident is **resolved or closed**
- When you want to **capture the fix** for the service desk or end users
- Before publishing to ServiceNow KB (human SME must approve)



### Real-world example

> A user reported: *"Email is slow when I attach a file."*  
> The engineer fixed it and closed **INC0000013**.  
> Now DIT wants a KB article so L1 can handle it next time without escalating.



### What you type (input)

```
Draft a KB article from INC0000013
```

Or list tickets first:

```
Show resolved incidents and draft a KB article from one of them
```

**MCP tools used:** `get_incident_for_kb_draft` or `get_resolved_incidents`

### What happens behind the scenes

1. Claude reads the closed incident from ServiceNow (description, close notes, category, etc.)
2. If close notes are thin, it also uses `demo_data/Demo_INC0000013_Resolution_Notes.md`
3. It writes a structured KB **draft** — not published to ServiceNow



### Example output

```markdown
# EMAIL is slow when an attachment is involved

## Symptoms
Email is slow when an attachment is involved.

## Likely cause
Not confirmed from incident data. [or from close_notes if present]

## Resolution steps
1. Confirm attachment size (limit: 10 MB for standard mail flow)
2. Ask user to send a plain-text email without attachment — confirm normal speed
3. If attachment-related: advise compressing file or using approved file-share link
...

## Escalation
Escalate to Email/Messaging team if issue persists after workaround.

---
*Draft — IT SME review required. Not published. Source: INC0000013*
```



### How it helps


| Before                         | After                                      |
| ------------------------------ | ------------------------------------------ |
| Fix buried in one ticket       | Reusable KB draft ready for SME review     |
| L1 escalates every time        | Clear steps for front-line support         |
| Manual copy-paste from tickets | Faster first draft from real incident data |


---



## Use Case 2 — Incident Status Communication Drafting



### The problem

During an outage (e.g. payroll server down), managers and business users keep asking: *"What's going on? When will it be fixed?"* Writing clear, consistent updates under pressure is hard — and you must not guess root cause or ETA.

### Where it fits

- **Active P1/P2 incidents** (critical/high priority)
- Before sending email, Teams message, or executive briefing
- Incident Manager reviews every draft before it goes out



### Real-world example

> **INC0007001** — *Employee payroll application server is down* (Priority 1).  
> HR and payroll teams need an update. The Incident Manager asks for a stakeholder comms draft.



### What you type (input)

```
Draft status comms for INC0007001
```

Or for all critical open incidents:

```
List high-priority incidents and draft status updates
```

**MCP tools used:** `get_incident_for_status_comms` or `list_high_priority_incidents`

### What happens behind the scenes

1. Claude fetches live incident fields: state, priority, description, assignment group, impact
2. It writes a professional update using **only** returned data
3. It never invents root cause, ETA, or "service restored" unless state confirms it



### Example output

```markdown
**Subject:** Service Update — Employee payroll application server is down

**Current status:** New

**Issue:**
Employee payroll application server is down.

**Business impact:**
Not confirmed from incident data.

**IT action:**
The [assignment_group] team is assigned.

**Next update:**
A further update will be provided within 30 minutes, or earlier if service is restored.

---
*Draft — pending Incident Manager review. Not sent. No ServiceNow record was modified.*
*Source: ServiceNow read-only MCP — INC0007001*
```



### How it helps


| Before                     | After                                                 |
| -------------------------- | ----------------------------------------------------- |
| Ad-hoc emails under stress | Consistent, safe draft in seconds                     |
| Risk of wrong ETA or RCA   | Only facts from ServiceNow — gaps say "Not confirmed" |
| IM rewrites from scratch   | IM edits draft instead of writing from zero           |


---



## Use Case 3 — Incident Post-Mortem Synthesis



### The problem

After a major outage, leadership wants a post-mortem: timeline, impact, root cause, and action items. ServiceNow tickets often have basic fields only — not a full story. Writing the document takes hours.

### Where it fits

- After a **significant incident** is resolved
- For outage reviews, RCA meetings, or audit documentation
- Incident Manager / DIT lead reviews before sharing



### Real-world example

> Payroll was down for ~2 hours (**INC0007001**).  
> The CIO asks: *"What happened, who was affected, and what are we doing to prevent a repeat?"*



### What you type (input)

```
Draft post-mortem for INC0007001 using demo notes
```

**MCP tool used:** `get_incident_for_post_mortem`

**Supporting file:** `demo_data/Demo_INC0007001_Resolution_Notes.md` (timeline, impact, corrective actions)

### What happens behind the scenes

1. Claude gets incident metadata from ServiceNow
2. It adds approved timeline and RCA context from demo resolution notes (when ticket fields are not enough)
3. It produces a structured post-mortem **draft** — not filed in ServiceNow



### Example output

```markdown
# Post-Mortem: INC0007001 — Employee payroll application server is down

## Timeline
- 09:10 — Incident opened (INC0007001)
- 09:25 — Hardware connectivity issue identified on application server
- 10:15 — Openspace support team engaged
- 11:00 — Service restored; users confirmed access

## Business impact
Payroll users could not access the application during the outage window.

## Root cause
Not confirmed from ServiceNow incident fields alone. Investigation noted server hardware alert gap.

## Corrective actions
1. Validate server-health alert thresholds
2. Review hardware monitoring coverage for payroll application tier
...

## Lessons learned
[Summary based on approved notes only]

---
*Draft — Incident Manager / DIT review required.*
```



### How it helps


| Before                              | After                                      |
| ----------------------------------- | ------------------------------------------ |
| Scattered notes in tickets and chat | One structured draft to refine             |
| RCA invented by AI (risky)          | RCA only from approved data — gaps flagged |
| Hours of manual writing             | Fast first draft for the review meeting    |


---



## Use Case 4 — Runbook and SOP Generation



### The problem

New joiners and L1 support don't know the standard steps for common tasks (shared folder access, email troubleshooting). Knowledge is tribal — senior engineers repeat the same instructions on every ticket.

### Where it fits

- Building **operational runbooks** and **SOPs** for the service desk
- After seeing **repeat incident patterns**
- Before putting procedures into the official ops wiki (DIT/IAM review required)



### Real-world example

> Every week, tickets arrive: *"Can't access shared folder"*, *"Access denied on file share"*.  
> DIT wants a standard runbook so anyone can follow the same IAM-approved steps.



### What you type (input)

```
Create a runbook for shared folder access issues
```

Or search KB first:

```
Search KB for email issues and draft an SOP
```

**MCP tools used:** `search_knowledge_articles` (and optionally `list_high_priority_incidents`)

**Supporting file:** `demo_data/Demo_IAM_Configuration_Notes.md`

### What happens behind the scenes

1. Claude searches ServiceNow KB **metadata** (titles, categories — not full article body)
2. For access/folder topics, it uses approved IAM steps from demo config notes
3. It outputs a step-by-step runbook **draft**



### Example output

```markdown
# Runbook: Shared Folder Access

## Purpose
Standard steps to restore user access to a shared network folder.

## Pre-checks
1. Confirm requester identity via corporate directory
2. Confirm folder name and required access level (read / read-write)

## Resolution steps
1. Verify approved access request exists in IAM queue
2. Add user to folder security group only via approved IAM workflow
3. Ask user to sign out and sign in (or wait 15 min for group sync)
4. Confirm user can access folder

## Escalation
Escalate to IAM team if group membership is correct but access still denied.

## Validation
User confirms issue resolved.

---
*Draft — DIT/IAM review required before operational use.*
```



### How it helps


| Before                     | After                               |
| -------------------------- | ----------------------------------- |
| Same answer typed 50 times | One runbook draft for the team      |
| Inconsistent IAM steps     | Steps aligned to approved workflow  |
| KB exists but hard to find | Search + structured SOP in one flow |


---



## Use Case 5 — SLA and Service-Desk Reporting



### The problem

Every Monday, the DIT manager wants a snapshot: how many open tickets, which categories are busiest, which teams are overloaded, any SLA concerns. Pulling this from ServiceNow manually takes time.

### Where it fits

- **Weekly or monthly** service desk reviews
- Ops stand-ups and management reporting
- Backlog and capacity planning conversations



### Real-world example

> It's Monday morning. The manager asks: *"Give me a summary of open incidents — categories, priorities, and assignment groups."*



### What you type (input)

```
Weekly service desk summary from open incidents
```

**MCP tool used:** `get_open_incident_category_summary`

**Optional:** `list_high_priority_incidents` to highlight P1/P2 items

### What happens behind the scenes

1. Claude fetches open/new incidents from ServiceNow (up to a limit, e.g. 25)
2. It aggregates counts by category, priority, and assignment group
3. It writes an executive-friendly **narrative draft** — not a formal SLA certification



### Example output

```markdown
# Weekly Service Desk Summary

**Total incidents reviewed:** 10
**Open incidents:** 10
**High/Critical:** 3 in Priority 1, 2 in Priority 2

## By category
- Inquiry / Help: 4
- Software: 3
- Network: 2
- Uncategorised: 1

## By assignment group
- Service Desk: 5
- Network: 3
- Application Dev: 2

## Key findings
- Network category shows 2 open items assigned to Network team.
- 3 Priority 1 incidents require immediate attention.

## SLA note
SLA breach status not confirmed from supplied data where made_sla is blank.
Counts reflect returned sample only (limit 25).

---
*Draft — DIT manager validation required.*
```



### How it helps


| Before                          | After                                                   |
| ------------------------------- | ------------------------------------------------------- |
| Manual exports and pivot tables | Narrative summary in one prompt                         |
| Over-claiming SLA breaches      | Honest limits — sample size and blank SLA fields stated |
| Delayed weekly report           | Quick draft for manager to validate and share           |


---



## Use Case 6 — Change Advisory Board (CAB) Preparation



### The problem

Before a production change goes to CAB, someone must prepare a brief: what is changing, risk, impact, implementation plan, rollback plan, and approval status. Copying fields from the change record into a readable document is tedious.

### Where it fits

- **Before CAB meetings** for normal/standard/emergency changes
- Change managers preparing reviewer packs
- Risk and impact summary for approvers



### Real-world example

> **CHG0000024** — *Clear BGP sessions on a Cisco router* is on this week's CAB agenda.  
> The change manager needs a one-page brief for the board.



### What you type (input)

```
Prepare CAB brief for CHG0000024
```

**MCP tool used:** `get_change_request_summary`

### What happens behind the scenes

1. Claude reads the change request from ServiceNow (description, risk, impact, plans, approval)
2. It formats a CAB-ready **draft brief**
3. It does not claim the change was approved or executed



### Example output

```markdown
# CAB Brief: CHG0000024 — Clear BGP sessions on a Cisco router

## Change summary
Clear BGP sessions on a Cisco router. Category: Network. Priority: [from record].

## Risk & impact
Risk: [from risk field] | Impact: [from impact field]

## Implementation plan
[from implementation_plan or: Not confirmed from data]

## Rollback plan
[from backout_plan or: Not confirmed from data]

## Approvals
[from approval field]

---
*Draft — CAB reviewer decision required. No change was executed.*
```



### How it helps


| Before                       | After                                           |
| ---------------------------- | ----------------------------------------------- |
| Manual copy from change form | Structured CAB brief in seconds                 |
| Missing rollback in the pack | Rollback section pulled from backout_plan field |
| Approvers read raw SN screen | Readable summary for the meeting                |


---



## How to test all use cases



### Step 1 — Confirm MCP is connected

In Claude Code, from the `servicenow-mcp-poc` folder:

```bash
claude
/mcp
```

You should see: `servicenow-dit-readonly` **— Connected — 8 tools**

### Step 2 — Run automated tool test

```bash
cd servicenow-mcp-poc
uv run python test_tools.py
```

Expected: **8/8 tools responded successfully**

### Step 3 — Test each skill with the prompts above

Use the **Quick reference** table at the top — one prompt per use case.

### What to check in every response

- Claude **called an MCP tool** (visible in the chat)
- Output ends with **Draft — [reviewer] required**
- No claim that anything was **sent, published, approved, or executed**
- Missing data says **"Not confirmed from incident/data"** — not invented

---



## Safety rules (all use cases)


| Rule                  | Why                                                                      |
| --------------------- | ------------------------------------------------------------------------ |
| **GET only**          | No ticket updates, no emails sent, no KB publish                         |
| **Draft only**        | Human IT/DIT review before any real action                               |
| **No invented facts** | No fake root cause, ETA, SLA breach, or resolution steps                 |
| **No PII**            | Caller names, emails, and work notes are not pulled                      |
| **Demo files**        | `demo_data/` supplements thin developer-instance data for POC demos only |


---



## Which use case when? (decision guide)

```text
Is the incident still OPEN and critical?
  → Use Case 2: Status Comms

Is the incident CLOSED and the fix should be reused?
  → Use Case 1: KB Article

Was it a MAJOR outage and you need a review document?
  → Use Case 3: Post-Mortem

Do people keep asking HOW to fix the same type of issue?
  → Use Case 4: Runbook / SOP

Do you need a WEEKLY snapshot of the backlog?
  → Use Case 5: SLA / Service-Desk Report

Is a CHANGE going to CAB?
  → Use Case 6: CAB Preparation
```

---



## Demo data files


| File                                            | Used by                  | Purpose                                |
| ----------------------------------------------- | ------------------------ | -------------------------------------- |
| `demo_data/Demo_INC0000013_Resolution_Notes.md` | KB Article (Use Case 1)  | Email attachment troubleshooting steps |
| `demo_data/Demo_INC0007001_Resolution_Notes.md` | Post-Mortem (Use Case 3) | Timeline, impact, corrective actions   |
| `demo_data/Demo_IAM_Configuration_Notes.md`     | Runbook (Use Case 4)     | Shared folder access standard process  |


These are **fictional POC supplements**. In production, approved resolution notes would come from your CMDB, work notes export, or internal wiki — not demo files.