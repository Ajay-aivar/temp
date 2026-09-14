# Demo IAM configuration notes (fictional, for POC only)

**Use with:** Runbook and SOP Generation skill

## Shared folder access — standard process

1. Confirm requester identity via corporate directory
2. Confirm folder name and required access level (read / read-write)
3. Verify approved access request exists in IAM queue
4. Add user to folder security group only via approved IAM workflow
5. Ask user to sign out and sign in (or wait 15 min for group sync)
6. Confirm user can access folder

## Escalation

Escalate to IAM team if group membership is correct but access still denied.

## Related incident patterns

- Unable to access shared folder
- Access denied on network file share
- SharePoint permission issue
