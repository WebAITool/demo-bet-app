# Development
FROM python:3.11 AS development

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m pip install --user pipx && \
    pipx install uv

COPY requirements.txt .

RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

COPY . .

CMD ["sleep", "infinity"]


# Production
FROM python:3.11-slim AS production

ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app

USER appuser

ENV PATH="/home/appuser/.local/bin:${PATH}"

RUN python -m pip install --user pipx && \
    pipx install uv

COPY requirements.txt .

RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
