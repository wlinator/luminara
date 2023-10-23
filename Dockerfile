FROM python:3.11
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y locales mariadb-client && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure locales

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

CMD [ "python", "./main.py" ]