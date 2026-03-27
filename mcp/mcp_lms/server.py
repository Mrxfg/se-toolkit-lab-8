"""Stdio MCP server exposing LMS backend operations as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_lms.client import LMSClient

_base_url: str = ""

server = Server("lms")

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


class _LabQuery(BaseModel):
    lab: str = Field(description="Lab identifier, e.g. 'lab-04'.")


class _TopLearnersQuery(_LabQuery):
    limit: int = Field(
        default=5, ge=1, description="Max learners to return (default 5)."
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_api_key() -> str:
    for name in ("NANOBOT_LMS_API_KEY", "LMS_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    raise RuntimeError(
        "LMS API key not configured. Set NANOBOT_LMS_API_KEY or LMS_API_KEY."
    )


def _client() -> LMSClient:
    if not _base_url:
        raise RuntimeError(
            "LMS backend URL not configured. Pass it as: python -m mcp_lms <base_url>"
        )
    return LMSClient(_base_url, _resolve_api_key())


def _text(data: BaseModel | Sequence[BaseModel]) -> list[TextContent]:
    """Serialize a pydantic model (or list of models) to a JSON text block."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = [item.model_dump() for item in data]
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _health(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().health_check())


async def _labs(_args: _NoArgs) -> list[TextContent]:
    items = await _client().get_items()
    return _text([i for i in items if i.type == "lab"])


async def _learners(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().get_learners())


async def _pass_rates(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_pass_rates(args.lab))


async def _timeline(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_timeline(args.lab))


async def _groups(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_groups(args.lab))


async def _top_learners(args: _TopLearnersQuery) -> list[TextContent]:
    return _text(await _client().get_top_learners(args.lab, limit=args.limit))


async def _completion_rate(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_completion_rate(args.lab))


async def _sync_pipeline(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().sync_pipeline())


# ---------------------------------------------------------------------------
# Registry: tool name -> (input model, handler, Tool definition)
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    # Pydantic puts definitions under $defs; flatten for MCP's JSON Schema expectation.
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (
        model,
        handler,
        Tool(name=name, description=description, inputSchema=schema),
    )


_register(
    "lms_health",
    "Check if the LMS backend is healthy and report the item count.",
    _NoArgs,
    _health,
)
_register("lms_labs", "List all labs available in the LMS.", _NoArgs, _labs)
_register(
    "lms_learners", "List all learners registered in the LMS.", _NoArgs, _learners
)
_register(
    "lms_pass_rates",
    "Get pass rates (avg score and attempt count per task) for a lab.",
    _LabQuery,
    _pass_rates,
)
_register(
    "lms_timeline",
    "Get submission timeline (date + submission count) for a lab.",
    _LabQuery,
    _timeline,
)
_register(
    "lms_groups",
    "Get group performance (avg score + student count per group) for a lab.",
    _LabQuery,
    _groups,
)
_register(
    "lms_top_learners",
    "Get top learners by average score for a lab.",
    _TopLearnersQuery,
    _top_learners,
)
_register(
    "lms_completion_rate",
    "Get completion rate (passed / total) for a lab.",
    _LabQuery,
    _completion_rate,
)
_register(
    "lms_sync_pipeline",
    "Trigger the LMS sync pipeline. May take a moment.",
    _NoArgs,
    _sync_pipeline,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main(base_url: str | None = None) -> None:
    global _base_url
    global VICTORIALOGS_URL, VICTORIATRACES_URL
    global VICTORIALOGS_URL, VICTORIATRACES_URL
    _base_url = base_url or os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    VICTORIALOGS_URL = os.environ.get("NANOBOT_LOGS_BASE_URL", "http://victorialogs:9428")
    VICTORIATRACES_URL = os.environ.get("NANOBOT_TRACES_BASE_URL", "http://victoriatraces:10428")
    VICTORIALOGS_URL = os.environ.get("NANOBOT_LOGS_BASE_URL", "http://victorialogs:9428")
    VICTORIATRACES_URL = os.environ.get("NANOBOT_TRACES_BASE_URL", "http://victoriatraces:10428")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())


# ---------------------------------------------------------------------------
# Observability tools — VictoriaLogs + VictoriaTraces
# ---------------------------------------------------------------------------

import httpx

VICTORIALOGS_URL = ""
VICTORIATRACES_URL = ""


class _LogsSearchArgs(BaseModel):
    query: str = Field(default="*", description="LogsQL query string, e.g. 'level:error'")
    limit: int = Field(default=20, ge=1, le=200, description="Max log entries to return.")
    time_range: str = Field(default="1h", description="Time range, e.g. '1h', '30m', '24h'.")


class _LogsErrorCountArgs(BaseModel):
    service: str = Field(default="", description="Service name to filter by. Empty = all.")
    time_range: str = Field(default="1h", description="Time range, e.g. '1h', '30m'.")


class _TracesListArgs(BaseModel):
    service: str = Field(default="Learning Management Service", description="Service name.")
    limit: int = Field(default=10, ge=1, le=100, description="Max traces to return.")


class _TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch.")


async def _logs_search(args: _LogsSearchArgs) -> list[TextContent]:
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    params = {"query": args.query, "limit": args.limit, "start": f"-{args.time_range}"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
    lines = [line for line in resp.text.strip().split("\n") if line]
    entries = []
    for line in lines:
        try:
            entries.append(json.loads(line))
        except Exception:
            entries.append({"raw": line})
    return [TextContent(type="text", text=json.dumps(entries, ensure_ascii=False))]


async def _logs_error_count(args: _LogsErrorCountArgs) -> list[TextContent]:
    if args.service:
        query = f'_stream:{{service.name="{args.service}"}} AND severity:ERROR'
    else:
        query = "severity:ERROR"
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    params = {"query": query, "limit": 200, "start": f"-{args.time_range}"}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
    lines = [line for line in resp.text.strip().split("\n") if line]
    count = len([l for l in lines if l])
    result = {"error_count": count, "service": args.service or "all", "time_range": args.time_range}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


async def _traces_list(args: _TracesListArgs) -> list[TextContent]:
    url = f"{VICTORIATRACES_URL}/jaeger/api/traces"
    params = {"service": args.service, "limit": args.limit}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
    data = resp.json()
    traces = data.get("data", [])
    simplified = []
    for t in traces:
        spans = t.get("spans", [])
        errors = sum(1 for s in spans if any(
            tag.get("key") == "error" and tag.get("value") for tag in s.get("tags", [])
        ))
        simplified.append({
            "traceID": t.get("traceID"),
            "spans": len(spans),
            "errors": errors,
        })
    return [TextContent(type="text", text=json.dumps(simplified, ensure_ascii=False))]


async def _traces_get(args: _TracesGetArgs) -> list[TextContent]:
    url = f"{VICTORIATRACES_URL}/jaeger/api/traces/{args.trace_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
    data = resp.json()
    traces = data.get("data", [])
    if not traces:
        return [TextContent(type="text", text=json.dumps({"error": "Trace not found"}))]
    t = traces[0]
    spans = t.get("spans", [])
    result = {
        "traceID": t.get("traceID"),
        "spans": [
            {
                "operationName": s.get("operationName"),
                "duration_ms": round(s.get("duration", 0) / 1000, 2),
                "tags": {tag["key"]: tag["value"] for tag in s.get("tags", [])},
            }
            for s in spans
        ],
    }
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


_register("logs_search", "Search structured logs in VictoriaLogs by LogsQL query and time range.", _LogsSearchArgs, _logs_search)
_register("logs_error_count", "Count error-level log entries for a service over a time window.", _LogsErrorCountArgs, _logs_error_count)
_register("traces_list", "List recent traces for a service from VictoriaTraces.", _TracesListArgs, _traces_list)
_register("traces_get", "Fetch a specific trace by ID from VictoriaTraces.", _TracesGetArgs, _traces_get)
