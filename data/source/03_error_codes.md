# Error Codes

## Error Response Format
All errors return a JSON body:

```json
{
  "error": {
    "code": "shipment_not_found",
    "message": "No shipment matches the given ID.",
    "request_id": "req_8f3a2b1c"
  }
}
```

Always log `request_id` when reporting an issue to support — it lets us trace the exact request server-side.

## Shipment Errors

| Code | HTTP Status | Meaning |
|---|---|---|
| `shipment_not_found` | 404 | No shipment exists with that ID for this workspace |
| `shipment_already_cancelled` | 409 | Attempted to modify a shipment that was already cancelled |
| `invalid_address` | 422 | Destination or origin address failed validation |
| `carrier_unavailable` | 503 | Selected carrier's service is temporarily down; retry later |

## Bulk Upload Errors
When using `POST /v2/shipments/bulk`, a partial failure is possible: some records in the batch succeed while others fail. The response includes a `results` array with a per-record status. A `carrier_unavailable` error on an individual record within a bulk request does NOT fail the whole batch — only that record is marked failed; the rest still process.

Note: this is different from a `carrier_unavailable` error on a single (non-bulk) shipment creation call, which does fail the whole request, since there's only one record to fail.

## Webhook Delivery Errors
Webhook errors are NOT returned in the API response — they appear in the Webhook Logs dashboard instead, since webhooks are asynchronous. Common webhook failure reasons:

- `endpoint_timeout` — your endpoint took longer than 5 seconds to respond
- `endpoint_unreachable` — DNS or connection failure
- `invalid_signature_response` — your endpoint returned a non-2xx status

Webhooks are retried up to 5 times with exponential backoff (1min, 5min, 30min, 2hr, 6hr), after which the delivery is marked permanently failed and must be manually replayed from the dashboard.
