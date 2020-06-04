FROM python:3.8

COPY . /consensus
WORKDIR /consensus

RUN pip install pipenv
RUN pipenv install --system --deploy
