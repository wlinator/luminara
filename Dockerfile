FROM python:3.12
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y locales mariadb-client && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure locales

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

CMD [ "poetry", "run", "python", "./Luminara.py" ]