FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY capsule ./capsule
COPY examples ./examples
COPY benchmarks ./benchmarks

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "capsule.api:app", "--host", "0.0.0.0", "--port", "8000"]
