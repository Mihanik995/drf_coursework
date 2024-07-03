FROM python:3

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY . /code

RUN poetry config virtualenvs.create false
RUN poetry install --no-root