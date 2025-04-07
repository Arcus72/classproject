FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml requirements.txt  ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# -----------------------------

FROM python:3.12-slim AS runner

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/src /app/src

RUN pip install --no-cache /wheels/* && rm -rf /wheels

EXPOSE 5000

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]
