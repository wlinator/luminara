FROM python:3.12-slim-bookworm
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales mariadb-client && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    pip cache purge

COPY . .

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

CMD [ "poetry", "run", "python", "-O", "./main.py" ]