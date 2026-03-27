# Observability Skill

## Available tools
- `logs_search` — search logs by LogsQL query and time range
- `logs_error_count` — count errors for a service over a time window
- `traces_list` — list recent traces for a service
- `traces_get` — fetch a specific trace by ID

## When user asks "What went wrong?" or "Check system health"
Follow this exact investigation sequence:
1. Call `logs_error_count` for all services (last 1h)
2. If errors > 0, call `logs_search` with `query="severity:ERROR"` to get details
3. Extract a `trace_id` from any log entry that has one
4. Call `traces_get` with that trace_id to see the full span hierarchy
5. Summarize findings in plain language: what failed, which service, what error, how long it took

## When user asks about errors generally
- Call `logs_error_count` first, then `logs_search` for details
- Always report: error count, service name, error message, and time

## Response format
- Concise summary, no raw JSON dumps
- Use bullet points for multiple errors
- Always mention if no errors found
