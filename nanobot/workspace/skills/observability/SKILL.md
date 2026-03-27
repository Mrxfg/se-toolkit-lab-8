# Observability Skill

You have access to logs and traces from the LMS backend via these tools:
- `logs_search` — search logs by LogsQL query and time range
- `logs_error_count` — count errors for a service over a time window
- `traces_list` — list recent traces for a service
- `traces_get` — fetch a specific trace by ID

## When to use

- User asks about errors, failures, or issues → call `logs_error_count` first, then `logs_search` with `query="severity:ERROR"` for details
- User asks about slow requests or latency → call `traces_list` and look at duration
- User asks "what happened" for a specific request → search logs for trace_id, then call `traces_get`
- If you find a trace_id in log entries, always offer to fetch the full trace

## Response format

- Summarize findings concisely — don't dump raw JSON
- Report error count, which service, and what the error event was
- For traces, report operation name and duration in ms
- If no errors found, say so clearly
