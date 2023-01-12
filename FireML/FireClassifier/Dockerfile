FROM python:3.9-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN groupadd ai && \
    useradd wildfire -G ai --create-home

USER wildfire

WORKDIR /home/wildfire/
COPY --chown=wildfire:ai . .

CMD ["python", "main.py"]
