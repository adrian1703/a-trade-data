FROM python:3.13.7-slim-bookworm

WORKDIR /a-trade-data-module

COPY ./app .
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system

CMD ["python", "./app/main.py"]