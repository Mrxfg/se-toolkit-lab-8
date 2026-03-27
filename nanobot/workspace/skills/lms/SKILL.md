# LMS Skills for Nanobot

## Available Tools
- lms_labs
- lms_health
- lms_learners
- lms_pass_rates
- lms_timeline
- lms_groups
- lms_top_learners
- lms_completion_rate
- lms_sync_pipeline

## When to Use Each Tool
- `lms_labs`: List all labs available in the LMS
- `lms_pass_rates`: Get pass rate for a specific lab
- `lms_timeline`: Track submissions over time
- `lms_sync_pipeline`: Trigger if data is outdated
- Other tools: Use for health checks, learner info, group performance

## Handling Missing Parameters
- Ask user for lab name if not provided
- Provide guidance or list options when unsure

## Response Formatting
- Use tables for multiple rows
- Summarize for health/status checks
- Be concise and clear
