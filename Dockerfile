FROM python:3.10-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py /app/

# Production stage
FROM base AS production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
