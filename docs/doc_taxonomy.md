# Documentation Taxonomy (for source_name / product_area metadata)

## Product Areas
- `auth` — API keys, OrAuth, key rotation, permission scopes
- `rate_limits` — Request limits, headers, backoff behavior
- `errors` — error codes, error response format, retry behavior
- `shipments` — core shipment CRUD, bulk operations
- `webhooks` — webhook config, delivery, retries, signatures
- `tracking` — tracking lookups, carrier status mapping

## Source Types
- `api_reference` — canonical technical docs (the 3 sample pages sent)
- `faq` — support-team-maintained Q&A (not yet exported, ~40 entries)
- `changelog` — dated API version changes (not yet exported)
- `slack_thread` — informal internal answers, LOWEST trust tier, needs manual review before ingesting since accuracy isn't guaranteed

## Metadata Fields Expected on Each Chunk
- `source_name` (e.g. "API Reference")
- `source_type` (one of the types above)
- `product_area` (one of the areas above)
- `url` (deep link to the doc, even if internal for now)
- `last_updated` (date, so stale answers can eventually be flagged)

Note: this generalizes the `doc.metadata["bank"]` pattern from your earlier project — same idea, renamed to fit us instead of hardcoded to a client name.
