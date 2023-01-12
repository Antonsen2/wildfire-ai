FROM python:3.9-slim AS builder

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM python:3.9-slim

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN groupadd api && \
    useradd wildfire -G api --create-home

USER wildfire

WORKDIR /home/wildfire/api
COPY --chown=wildfire:api . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
