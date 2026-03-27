FROM python:3.12-slim-bookworm

RUN pip install uv

WORKDIR /app

COPY . /app/nanobot/
COPY --from=workspace mcp/ /app/mcp/
COPY --from=workspace nanobot-websocket-channel/ /app/nanobot-websocket-channel/

RUN uv pip install --system nanobot-ai
RUN uv pip install --system /app/mcp
RUN uv pip install --system /app/nanobot-websocket-channel

CMD ["python", "/app/nanobot/entrypoint.py"]
