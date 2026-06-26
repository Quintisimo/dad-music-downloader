FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.11-slim

COPY --from=denoland/deno:bin /deno /usr/local/bin/deno
COPY --from=mwader/static-ffmpeg:latest /ffmpeg /ffprobe /usr/local/bin/

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "src/main.py"]
