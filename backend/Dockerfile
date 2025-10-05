FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock README.md ./
COPY ./app ./app
RUN uv sync --frozen --no-cache
EXPOSE 80
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]