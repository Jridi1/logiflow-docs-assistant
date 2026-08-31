# Rate Limits

## Standard Limits by Plan

| Plan | Requests / minute | Burst allowance |
|---|---|---|
| Starter | 60 | 10 |
| Growth | 300 | 50 |
| Enterprise | 1200 | 200 |

Rate limits are applied per API key, not per workspace. If you have two active keys during a rotation window (see Authentication page), each key gets its own limit — they are not shared or combined.

## Endpoint-Specific Overrides
Some endpoints have their own limits that override the plan default, because they're more expensive to process:

- `POST /v2/shipments/bulk` — capped at 10 requests/minute regardless of plan, since each request can contain up to 500 shipment records.
- `GET /v2/tracking/{id}` — capped at 600 requests/minute on all plans (higher than the plan default on Starter, since tracking lookups are cheap).
- `POST /v2/webhooks/test` — capped at 5 requests/minute to prevent webhook spam during testing.

## What Happens When You're Rate Limited
You'll receive a `429 rate_limited` response with a `Retry-After` header (in seconds). We recommend exponential backoff rather than retrying immediately at the `Retry-After` boundary, since many clients retry simultaneously and cause a thundering-herd effect right at that mark.

## Rate Limit Headers
Every response (not just 429s) includes:

```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 287
X-RateLimit-Reset: 1719430200
```

`X-RateLimit-Reset` is a Unix timestamp, not a countdown in seconds — this trips people up because it looks similar to `Retry-After`, which IS in seconds.

## Increasing Your Limit
Growth and Enterprise plans can request a temporary limit increase (e.g. for a data migration) by contacting support at least 48 hours in advance. Starter plan limits are fixed and cannot be temporarily increased without upgrading the plan.
