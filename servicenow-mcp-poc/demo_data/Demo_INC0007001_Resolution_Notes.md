# Demo resolution notes — INC0007001 (fictional, for POC only)

**Incident:** Employee payroll application server is down  
**Use with:** Post-Mortem Synthesis skill

## Timeline (approved for demo)

- 09:10 — Incident opened (INC0007001)
- 09:25 — Hardware connectivity issue identified on application server
- 10:15 — Openspace support team engaged
- 11:00 — Service restored; users confirmed access

## Business impact (demo)

Payroll users could not access the application during the outage window.

## Root cause

Not confirmed from ServiceNow incident fields alone. Investigation noted server hardware alert gap.

## Corrective actions (draft)

1. Validate server-health alert thresholds
2. Review hardware monitoring coverage for payroll application tier
3. Document recovery procedure in runbook
4. Schedule resilience review with DIT
