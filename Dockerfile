# ---- Étape 1 : dépendances (cache optimisé) ----
FROM python:3.12-slim AS deps

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

RUN pip install --no-cache-dir poetry==2.4.2

WORKDIR /app
COPY pyproject.toml poetry.lock README.md ./
COPY src ./src
RUN poetry install --only main --no-interaction --no-ansi

# ---- Étape 2 : image finale, sans outils de build ----
FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# L'application tourne en non-root (bonne pratique de sécurité).
RUN useradd --create-home --uid 10001 appuser

WORKDIR /app
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY --chown=appuser:appuser src ./src

USER appuser
EXPOSE 8000

CMD ["uvicorn", "bttf.api:app", "--host", "0.0.0.0", "--port", "8000"]
