FROM python:3.11.6-slim-bullseye as python

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "--factory", "src.main:get_app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8003", "--reload"]
