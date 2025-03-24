FROM python:3.12-alpine AS build

WORKDIR /app

COPY . /app

RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine

WORKDIR /app

COPY --from=build /app /app
COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "-m", "app"]