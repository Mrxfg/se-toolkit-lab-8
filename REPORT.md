# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
**Question:** What is 2+2?
**Answer:** 2 + 2 = 4

**Question:** What is the agentic loop?
**Answer:** The agentic loop is the iterative cycle that autonomous AI agents follow to accomplish tasks:

1. **Perceive** — Gather information from the environment (observations, user input, tool outputs)
2. **Think/Reason** — Process information, plan next steps, make decisions
3. **Act** — Execute actions (call tools, modify files, send messages, run commands)
4. **Observe** — Receive feedback from the action's outcome
5. **Repeat** — Continue until the goal is achieved or a stopping condition is met

Perceive → Think → Act → Observe → [Done?] → (loop back if not done)

> This loop is what distinguishes an agent from a simple chatbot—agents can take iterative actions toward a goal rather than just responding once.

**Question:** What labs are available in our LMS?
**Answer:** At this stage, the agent does not know (no tools connected yet).


## Task 1B — Agent with LMS tools
Query: "What labs are available?"

Response from nanobot:

| # | Lab Title                                                | Tasks |
|---|----------------------------------------------------------|-------|
| 1 | Lab 01 – Products, Architecture & Roles                  | 9     |
| 2 | Lab 02 — Run, Fix, and Deploy a Backend Service         | 8     |
| 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy | 7     |
| 4 | Lab 04 — Testing, Front-end, and AI Agents              | 5     |
| 5 | Lab 05 — Data Pipeline and Analytics Dashboard          | 5     |
| 6 | Lab 06 — Build Your Own Agent                            | 4     |
| 7 | Lab 07 — Build a Client with an AI Coding Agent         | 5     |
| 8 | lab-08                                                   | 5     |

### Summary

- Total Labs: 8
- Total Tasks: 48
- Total Learners: 258
- Total Interactions (submissions): 14,320

You can now query the nanobot agent for:

- "Show me the pass rates for Lab 04"
- "Which lab has the lowest completion rate?"
- "Who are the top learners in Lab 01?"




## Task 1C — Skill prompt

**Question:** Show me the scores
**Answer:** Agent asks which lab if not specified and shows overview table with Avg Score, Students, Submissions. Example output:

| Lab | Avg Score | Students | Submissions |
|-----|-----------|----------|-------------|
| Lab 01 – Products, Architecture & Roles | 80.17% | 258 | 3,916 |
| Lab 02 — Run, Fix, and Deploy a Backend Service | 64.45% | 147 | 541 |
| Lab 03 — Backend API: Explore, Debug, Implement, Deploy | 61.75% | 174 | 834 |
| Lab 04 — Testing, Front-end, and AI Agents | 60.11% | 246 | 1,462 |
| Lab 05 — Data Pipeline and Analytics Dashboard | 68.49% | 250 | 1,337 |
| Lab 06 — Build Your Own Agent | 50.92% | 245 | 3,175 |
| Lab 07 — Build a Client with an AI Coding Agent | 67.43% | 237 | 2,733 |
| lab-08 | 69.58% | 56 | 322 |


## Task 2A — Deployed agent
Nanobot gateway started successfully:
```
nanobot-1 | 🐈 Starting nanobot gateway version 0.1.4.post6 on port 18790...
```


## Task 2B — Web client


WebSocket test:
```
{"type":"text","content":"Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n...","format":"markdown"}
```

Flutter client accessible at http://10.93.25.213:42002/flutter — agent responds to messages via WebSocket channel.
## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

- **Scenario:** The Nanobot system was launched and the 'What went wrong?' query was sent.
- **Agent response:** Error: Internal Server Error
- **Note:** The Nanobot identified a backend error. The response is brief and indicates an internal issue.
- **Screenshot:** \`ac885c56-d5e9-4598-a501-399bb8c5194e.png\`

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
