# backend/Dockerfile
# Multi-stage build with uv and Python

ARG REGISTRY_PREFIX_DOCKER_HUB

# --- Stage 1: build application ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy root-level pyproject.toml and uv.lock from repo root
COPY pyproject.toml uv.lock /app/

# Backend package sync
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package lms-backend

# Copy backend source code
COPY . /app/backend

# Sync again with uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package lms-backend

# Install OpenTelemetry auto-instrumentation
RUN /app/.venv/bin/opentelemetry-bootstrap -a install

# --- Stage 2: final image ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Create non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy built app from builder stage
COPY --from=builder --chown=nonroot:nonroot /app /app

# Set Python and backend paths
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/backend"

USER nonroot
WORKDIR /app

# Run backend with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", "uvicorn", "backend.app.main:app"]
