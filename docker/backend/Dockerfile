FROM python:3.9-slim-bookworm AS base
LABEL maintainer="Jmunoz"


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

FROM base AS builder
ARG BUILD_DEPS="g++ gcc libc-dev python3-dev libpq-dev curl unzip"


RUN apt-get update && \
    apt-get install -y --no-install-recommends $BUILD_DEPS && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN mkdir /backend
WORKDIR /backend


COPY ./requirements.txt /backend/requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

COPY ./backend /backend

FROM base


ARG RUNTIME_DEPS="libnss3 libglib2.0-dev xvfb libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm1 libasound2 python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 libgeos-dev libpq-dev wait-for-it"

RUN apt-get update && \
    apt-get install -y --no-install-recommends $RUNTIME_DEPS && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


WORKDIR /backend

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /backend /backend

COPY ./docker/backend/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]