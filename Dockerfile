FROM python:3.7

RUN pip3 install "pip==22.1.2" "pipenv==2022.6.7"

RUN mkdir /exabel
WORKDIR /exabel

COPY Pipfile /exabel
COPY Pipfile.lock /exabel
RUN pipenv sync

COPY . /exabel
