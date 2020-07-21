FROM python:3.8.2-alpine3.10

WORKDIR /app

RUN apk add --update --no-cache \
        build-base \
        python3-dev \
        libffi-dev \
        openssl-dev \
        && python3 -m pip install \
        cryptography==2.9.2 \
        && apk del \
        build-base \
        libffi-dev \
        openssl-dev \
        python3-dev

COPY ./py ./py

ENTRYPOINT [ "/app/py/main.py" ]
