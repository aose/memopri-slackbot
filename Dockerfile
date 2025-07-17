FROM python:3.13-bookworm

RUN pip3 install uv

RUN apt update && apt install -y fonts-noto-cjk

COPY ./app /app

WORKDIR /app

RUN uv sync

CMD ["uv", "run", "slack-bot.py"]