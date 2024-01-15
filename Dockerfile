FROM python:3.8

RUN pip3 install "pip==23.2.1" "pipenv==2023.9.8"

RUN mkdir /exabel
WORKDIR /exabel

COPY Pipfile /exabel
COPY Pipfile.lock /exabel
RUN pipenv sync

COPY . /exabel
