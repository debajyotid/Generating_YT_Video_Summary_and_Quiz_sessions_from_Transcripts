FROM python:3.10-slim AS base

FROM base AS builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM base
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
