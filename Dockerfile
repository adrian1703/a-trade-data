FROM python:3.13.7-slim-bookworm

WORKDIR /a-trade-data-module

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system

COPY ./app ./app
COPY ./openapi_server ./openapi_server
COPY ./a-trade-shared-resources ./a-trade-shared-resources

ENV PYTHONPATH=.

CMD ["python", "-u", "app/__main__.py"]