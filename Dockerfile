FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app
COPY . .

RUN uv sync --python=3.14 --extra=dev

CMD ["uv", "run", "uvicorn", "main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8000"]
