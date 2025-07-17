FROM ghcr.io/astral-sh/uv:bookworm-slim

RUN apt update && apt install -y --no-install-recommends \
    fonts-noto-cjk \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY ./app /app

WORKDIR /app

RUN uv sync

CMD ["uv", "run", "slack-bot.py"]