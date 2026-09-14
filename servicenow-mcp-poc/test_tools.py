"""Test all MCP tools against the configured ServiceNow developer instance."""

import asyncio
import sys

from dotenv import load_dotenv

load_dotenv(".env")


async def run_tests() -> int:
    from server import (
        get_change_request_summary,
        get_incident_for_kb_draft,
        get_incident_for_post_mortem,
        get_incident_for_status_comms,
        get_open_incident_category_summary,
        get_resolved_incidents,
        list_high_priority_incidents,
        search_knowledge_articles,
    )

    tests = [
        ("list_high_priority_incidents", lambda: list_high_priority_incidents(3)),
        ("get_incident_for_status_comms", lambda: get_incident_for_status_comms("INC0007001")),
        ("get_resolved_incidents", lambda: get_resolved_incidents(3)),
        ("get_incident_for_kb_draft", lambda: get_incident_for_kb_draft("INC0000013")),
        ("search_knowledge_articles", lambda: search_knowledge_articles("email", 3)),
        ("get_incident_for_post_mortem", lambda: get_incident_for_post_mortem("INC0007001")),
        ("get_open_incident_category_summary", lambda: get_open_incident_category_summary(10)),
        ("get_change_request_summary", lambda: get_change_request_summary("CHG0000024")),
    ]

    passed = 0
    for name, fn in tests:
        try:
            result = await fn()
            use_case = result.get("use_case", "?")
            ok = (
                "count" in result
                or result.get("found") is True
                or "total_open_or_new_incidents_returned" in result
            )
            status = "OK" if ok else "WARN"
            detail = result.get(
                "count",
                result.get("found", result.get("total_open_or_new_incidents_returned", "")),
            )
            print(f"  [{status}] {name} — {use_case} — {detail}")
            passed += 1
        except Exception as exc:
            print(f"  [FAIL] {name} — {exc}")

    print(f"\n{passed}/{len(tests)} tools responded successfully")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run_tests()))
