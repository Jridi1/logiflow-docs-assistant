# Authentication

## Overview
All requests to the LogiFlow API must be authenticated using an API key. Keys are issued per workspace from the Developer Settings page.

## API Key Authentication
Include your API key in the `Authorization` header of every request:

```
Authorization: Bearer lf_live_xxxxxxxxxxxxxxxxxxxx
```

Keys are prefixed with `lf_live_` for production keys and `lf_test_` for sandbox keys. Sandbox keys only work against `https://sandbox-api.logiflow.io`, not the production endpoint.

## Key Rotation
API keys do not expire automatically. We recommend rotating keys every 90 days. You can have up to 2 active keys per workspace at once, which allows a grace period when rotating: generate the new key, update your integration, then revoke the old one.

## OAuth2 (Partner Integrations Only)
Partner-tier accounts (not standard API customers) may use OAuth2 client credentials flow instead of static API keys. This requires a separate application registration and is not available on Starter or Growth plans. Contact your account manager if you believe you need this.

## Common Authentication Errors

| HTTP Status | Error Code | Meaning |
|---|---|---|
| 401 | `invalid_api_key` | Key is malformed, revoked, or doesn't exist |
| 401 | `expired_test_key` | Sandbox key used against production, or vice versa |
| 403 | `insufficient_scope` | Key is valid but lacks permission for this endpoint |
| 429 | `rate_limited` | Too many requests — see Rate Limits page |

## Losing / Resetting a Key
If a key is compromised, revoke it immediately from Developer Settings → API Keys → Revoke. There is no way to "reset" a key to a previous value — revoking is permanent and a new key must be generated.
