# Sample Support Questions (for retrieval regression tests)

These are real-ish recurring questions from our support queue. Some are intentionally phrased differently but should retrieve the SAME underlying answer — this is the exact retrieval-consistency problem you flagged from your N26 project, and we want your bot to handle it better this time.

## Group A — same underlying answer, different phrasing
1. "What's the rate limit on the bulk shipment endpoint?"
2. "How many bulk shipment requests can I send per minute?"
3. "Why am I getting rate limited on `/v2/shipments/bulk` even though I'm on Enterprise?"
   → All three should converge on: 10 req/min flat cap, regardless of plan.

## Group B — same underlying answer, different phrasing
4. "Does one failed shipment break my whole bulk upload?"
5. "If a carrier is down during a bulk import, does the entire batch fail?"
   → Should converge on: no, only that record fails, in bulk requests only.

## Group C — trap question (should NOT be answered from bulk logic)
6. "A single shipment I created failed because the carrier was unavailable — do I need to recreate it or does it auto-retry?"
   → This is a single (non-bulk) call, so the bulk partial-failure behavior does NOT apply. A bot confusing these two would be exactly the kind of contradiction bug from before.

## Group D — should trigger honest refusal (not in provided docs)
7. "Can I get a volume discount on my Enterprise plan?"
8. "Is there a Python SDK or do I have to call the REST API directly?"
9. "What's your uptime SLA?"
   → None of these are covered in the 3 sample pages. Bot should say it doesn't know / isn't in scope, NOT guess.

## Group E — genuinely ambiguous headers, easy to mix up
10. "How do I know when my rate limit resets?"
    → Tests whether the bot correctly distinguishes `X-RateLimit-Reset` (Unix timestamp) from `Retry-After` (seconds) — these get confused constantly.
