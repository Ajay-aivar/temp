"""Read-only ServiceNow MCP server — Pod Charlie DIT use cases."""

import os
from collections import Counter
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(Path(__file__).resolve().parent / ".env")

mcp = FastMCP(
    "servicenow-dit-readonly",
    instructions=(
        "Read-only ServiceNow data for DIT draft outputs: status comms, KB articles, "
        "runbooks, post-mortems, SLA reports, and CAB briefs. "
        "Use returned fields only. Do not claim records were changed or messages sent."
    ),
)

INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL", "").rstrip("/")
USERNAME = os.getenv("SERVICENOW_USERNAME", "")
PASSWORD = os.getenv("SERVICENOW_PASSWORD", "")
VERIFY_SSL = os.getenv("SERVICENOW_VERIFY_SSL", "true").lower() == "true"
MAX_LIMIT = 25

READONLY_NOTE = (
    "Read-only ServiceNow data. Output is a draft for human IT/DIT review. "
    "No records were created, modified, assigned, resolved, closed, or sent."
)

# --- Field allowlists per use case ---

OPERATIONAL_FIELDS = [
    "number", "short_description", "priority", "state", "category",
    "assignment_group", "opened_at", "impact", "urgency", "business_service",
]

RESOLVED_FIELDS = [
    "number", "short_description", "category", "state", "priority",
    "close_code", "close_notes", "assignment_group", "opened_at", "resolved_at",
]

SLA_FIELDS = [
    "number", "priority", "state", "category", "opened_at",
    "resolved_at", "assignment_group", "made_sla",
]

KNOWLEDGE_FIELDS = [
    "number", "short_description", "workflow_state", "kb_category", "topic", "active",
]

CHANGE_FIELDS = [
    "number", "short_description", "state", "priority", "risk", "impact",
    "category", "assignment_group", "start_date", "end_date",
    "justification", "implementation_plan", "backout_plan", "approval",
]


def validate_config() -> None:
    if not INSTANCE_URL or not USERNAME or not PASSWORD:
        raise RuntimeError(
            "Missing ServiceNow configuration. "
            "Set SERVICENOW_INSTANCE_URL, SERVICENOW_USERNAME, "
            "and SERVICENOW_PASSWORD in .env."
        )
    if not INSTANCE_URL.startswith("https://"):
        raise RuntimeError("SERVICENOW_INSTANCE_URL must start with https://")


def clamp_limit(limit: int) -> int:
    return max(1, min(limit, MAX_LIMIT))


async def fetch_table(
    table: str,
    field_names: list[str],
    *,
    encoded_query: str = "",
    limit: int = 10,
) -> list[dict[str, Any]]:
    validate_config()
    params: dict[str, str] = {
        "sysparm_fields": ",".join(field_names),
        "sysparm_display_value": "true",
        "sysparm_exclude_reference_link": "true",
        "sysparm_limit": str(clamp_limit(limit)),
    }
    if encoded_query:
        params["sysparm_query"] = encoded_query

    url = f"{INSTANCE_URL}/api/now/table/{table}"
    try:
        async with httpx.AsyncClient(
            auth=(USERNAME, PASSWORD), timeout=20.0, verify=VERIFY_SSL,
        ) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"ServiceNow API returned HTTP {exc.response.status_code} for '{table}'. "
            "Check credentials, roles, and query."
        ) from exc
    except httpx.RequestError as exc:
        raise RuntimeError(
            "Could not connect to ServiceNow. Check SERVICENOW_INSTANCE_URL."
        ) from exc

    records = response.json().get("result", [])
    if not isinstance(records, list):
        raise RuntimeError("Unexpected ServiceNow response format.")
    return records


def clean_record(record: dict[str, Any], field_names: list[str]) -> dict[str, str]:
    return {name: str(record.get(name, "") or "").strip() for name in field_names}


def tool_response(use_case: str, payload: dict[str, Any], *, limitation: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {"use_case": use_case, **payload, "note": READONLY_NOTE}
    if limitation:
        result["data_limitation"] = limitation
    return result


# --- Use Case 2: Incident Status Communication Drafting ---

@mcp.tool()
async def list_high_priority_incidents(limit: int = 10) -> dict[str, Any]:
    """Open/new priority 1 and 2 incidents for status communication drafting. Read-only."""
    records = await fetch_table(
        "incident", OPERATIONAL_FIELDS,
        encoded_query="priorityIN1,2^stateNOT IN6,7", limit=limit,
    )
    return tool_response(
        "Incident Status Communication Drafting",
        {"count": len(records), "incidents": [clean_record(r, OPERATIONAL_FIELDS) for r in records]},
        limitation="Do not invent root cause, ETA, or business impact.",
    )


@mcp.tool()
async def get_incident_for_status_comms(incident_number: str) -> dict[str, Any]:
    """One incident by number (e.g. INC0007001) for stakeholder status comms draft. Read-only."""
    incident_number = incident_number.strip().upper()
    if not incident_number.startswith("INC"):
        raise ValueError("incident_number must look like INC0007001.")

    records = await fetch_table(
        "incident", OPERATIONAL_FIELDS,
        encoded_query=f"number={incident_number}", limit=1,
    )
    if not records:
        return tool_response(
            "Incident Status Communication Drafting",
            {"found": False, "incident_number": incident_number,
             "message": "No incident found."},
        )
    return tool_response(
        "Incident Status Communication Drafting",
        {"found": True, "incident": clean_record(records[0], OPERATIONAL_FIELDS)},
        limitation="Do not invent root cause, ETA, resolution, or business impact.",
    )


# --- Use Case 1: KB Article Drafting from Resolved Tickets ---

@mcp.tool()
async def get_resolved_incidents(limit: int = 10) -> dict[str, Any]:
    """Resolved/closed incidents for KB article drafting. Read-only."""
    records = await fetch_table(
        "incident", RESOLVED_FIELDS,
        encoded_query="stateIN6,7", limit=limit,
    )
    return tool_response(
        "KB Article Drafting from Resolved Tickets",
        {"count": len(records), "incidents": [clean_record(r, RESOLVED_FIELDS) for r in records]},
        limitation=(
            "close_notes may be empty on developer instance. "
            "Combine with demo_data/ resolution notes when needed."
        ),
    )


@mcp.tool()
async def get_incident_for_kb_draft(incident_number: str) -> dict[str, Any]:
    """One resolved incident by number for KB article drafting. Example: INC0000013. Read-only."""
    incident_number = incident_number.strip().upper()
    if not incident_number.startswith("INC"):
        raise ValueError("incident_number must look like INC0000013.")

    records = await fetch_table(
        "incident", RESOLVED_FIELDS,
        encoded_query=f"number={incident_number}", limit=1,
    )
    if not records:
        return tool_response(
            "KB Article Drafting from Resolved Tickets",
            {"found": False, "incident_number": incident_number,
             "message": "No incident found."},
        )
    return tool_response(
        "KB Article Drafting from Resolved Tickets",
        {"found": True, "incident": clean_record(records[0], RESOLVED_FIELDS)},
        limitation="Do not invent resolution steps not in close_notes or approved demo files.",
    )


# --- Use Case 4: Runbook and SOP Generation ---

@mcp.tool()
async def search_knowledge_articles(query: str, limit: int = 10) -> dict[str, Any]:
    """Search KB article metadata for runbook/SOP context. Body text not returned. Read-only."""
    query = query.strip()
    if not query:
        raise ValueError("query must not be empty.")
    if len(query) > 100:
        raise ValueError("query must be 100 characters or fewer.")

    safe = query.replace("^", "").replace(",", " ")
    records = await fetch_table(
        "kb_knowledge", KNOWLEDGE_FIELDS,
        encoded_query=f"short_descriptionLIKE{safe}^ORtopicLIKE{safe}",
        limit=limit,
    )
    return tool_response(
        "Runbook and SOP Generation",
        {"query": query, "count": len(records),
         "articles": [clean_record(r, KNOWLEDGE_FIELDS) for r in records]},
        limitation="Article body not returned. Use with demo_data/ config notes for full runbooks.",
    )


# --- Use Case 3: Incident Post-Mortem Synthesis ---

@mcp.tool()
async def get_incident_for_post_mortem(incident_number: str) -> dict[str, Any]:
    """One incident by number for post-mortem draft input. Example: INC0007001. Read-only."""
    incident_number = incident_number.strip().upper()
    if not incident_number.startswith("INC"):
        raise ValueError("incident_number must look like INC0007001.")

    records = await fetch_table(
        "incident", OPERATIONAL_FIELDS,
        encoded_query=f"number={incident_number}", limit=1,
    )
    if not records:
        return tool_response(
            "Incident Post-Mortem Synthesis",
            {"found": False, "incident_number": incident_number,
             "message": "No incident found."},
        )
    return tool_response(
        "Incident Post-Mortem Synthesis",
        {"found": True, "incident": clean_record(records[0], OPERATIONAL_FIELDS)},
        limitation=(
            "Timeline and root cause not in API fields. "
            "Combine with demo_data/ resolution notes. Do not invent RCA."
        ),
    )


# --- Use Case 5: SLA and Service-Desk Reporting ---

@mcp.tool()
async def get_open_incident_category_summary(limit: int = 25) -> dict[str, Any]:
    """Open/new incident aggregates for weekly SLA and service-desk reporting. Read-only."""
    records = await fetch_table(
        "incident", SLA_FIELDS,
        encoded_query="stateNOT IN6,7", limit=limit,
    )
    incidents = [clean_record(r, SLA_FIELDS) for r in records]
    categories = Counter(i["category"] or "Uncategorised" for i in incidents)
    priorities = Counter(i["priority"] or "Not specified" for i in incidents)
    groups = Counter(i["assignment_group"] or "Unassigned" for i in incidents)
    sla_breached = [i for i in incidents if i["made_sla"].lower() == "false"]

    return tool_response(
        "SLA and Service-Desk Reporting",
        {
            "total_open_or_new_incidents_returned": len(incidents),
            "incidents_by_category": dict(categories),
            "incidents_by_priority": dict(priorities),
            "incidents_by_assignment_group": dict(groups),
            "sla_breach_count_in_sample": len(sla_breached),
            "sample_incidents": incidents,
        },
        limitation=(
            "Counts reflect returned records up to limit only. "
            "If made_sla is blank, SLA breach status is not confirmed."
        ),
    )


# --- Use Case 6: Change Advisory Board Preparation ---

@mcp.tool()
async def get_change_request_summary(change_number: str) -> dict[str, Any]:
    """One change request by number for CAB preparation draft. Example: CHG0000024. Read-only."""
    change_number = change_number.strip().upper()
    if not change_number.startswith("CHG"):
        raise ValueError("change_number must look like CHG0000024.")

    records = await fetch_table(
        "change_request", CHANGE_FIELDS,
        encoded_query=f"number={change_number}", limit=1,
    )
    if not records:
        return tool_response(
            "Change Advisory Board Preparation",
            {"found": False, "change_number": change_number,
             "message": "No change request found."},
            limitation="Developer instances may have limited change_request sample data.",
        )
    return tool_response(
        "Change Advisory Board Preparation",
        {"found": True, "change_request": clean_record(records[0], CHANGE_FIELDS)},
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
