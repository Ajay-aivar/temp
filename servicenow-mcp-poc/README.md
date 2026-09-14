# ServiceNow DIT Read-Only MCP (Pod Charlie POC)

One read-only MCP server + six Claude Skills for Syngene DIT use cases.

```text
ServiceNow (GET only) → MCP server (8 tools) → Claude Skills → Draft output → Human review
```

See **[USECASES_GUIDE.md](USECASES_GUIDE.md)** for a plain-language explanation of each use case with examples, inputs, and expected outputs.

## Use cases

| # | Use case | MCP tool(s) | Skill |
|---|----------|-------------|-------|
| 1 | KB Article Drafting | `get_resolved_incidents`, `get_incident_for_kb_draft` | `kb-article-from-ticket` |
| 2 | Incident Status Comms | `list_high_priority_incidents`, `get_incident_for_status_comms` | `incident-status-comms` |
| 3 | Post-Mortem Synthesis | `get_incident_for_post_mortem` | `incident-post-mortem` |
| 4 | Runbook / SOP Generation | `search_knowledge_articles` | `runbook-sop-generator` |
| 5 | SLA & Service-Desk Reporting | `get_open_incident_category_summary` | `sla-service-desk-report` |
| 6 | CAB Preparation | `get_change_request_summary` | `cab-preparation` |

## Setup

```bash
cd servicenow-mcp-poc
uv sync
cp .env.example .env   # configure admin credentials
```

## Test all tools

```bash
uv run python test_tools.py
```

## MCP Inspector

```bash
./dev-inspector.sh
```

Open http://127.0.0.1:6274 → Connect → Tools (8 tools).

## Claude Code

```bash
claude
/mcp   → servicenow-dit-readonly — Connected — 8 tools
```

### Example prompts

| Use case | Prompt |
|----------|--------|
| Status comms | `Draft status comms for INC0007001` |
| KB article | `Draft a KB article from INC0000013` |
| Runbook | `Create a runbook for shared folder access issues` |
| Post-mortem | `Draft post-mortem for INC0007001 using demo notes` |
| SLA report | `Weekly service desk summary from open incidents` |
| CAB | `Prepare CAB brief for CHG0000024` |

## Demo data

`demo_data/` — fictional resolution/config notes when PDI sample data is thin.

## Safety

- GET only — no writes, no auto-send, no KB publish
- Field allowlists per use case
- All output is draft — human IT/DIT review required
