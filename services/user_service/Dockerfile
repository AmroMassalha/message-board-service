# Stage 1: Build stage
FROM python:3.11.3-slim AS base

WORKDIR /app

# Install dependencies
COPY ../../requirements.txt .
RUN apt-get update && apt-get install -y curl
RUN pip install -r requirements.txt

COPY ../../foundations/ ./foundations/

# Stage 2: Build stage
FROM base AS builder

COPY ../../services/user_service/ ./user_service/

# Stage 3: Final image
FROM base

COPY --from=builder /app /app

WORKDIR /app/user_service

ENV PYTHONPATH /app

RUN python -m unittest discover -s tests/ -p *_test.py

CMD ["python", "app.py"]
