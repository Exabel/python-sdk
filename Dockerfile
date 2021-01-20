FROM python:3.6

RUN pip3 install "pip==20.1.1" "pipenv==2020.6.2"

RUN mkdir /exabel
WORKDIR /exabel

COPY Pipfile /exabel
COPY Pipfile.lock /exabel
RUN pipenv sync

COPY . /exabel
