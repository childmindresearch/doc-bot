FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

EXPOSE 8080

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-cache 

COPY ./app ./app

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8080"]