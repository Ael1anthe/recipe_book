FROM python:3.12 AS requirements-stage
WORKDIR /tmp

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /tmp/

ARG INSTALL_DEV=false
RUN bash -c "if\
                 [ $INSTALL_DEV == 'true' ] ;\
             then\
                 poetry export --without-hashes --with dev -f requirements.txt -o requirements.txt ;\
             else\
                 poetry export --without-hashes -f requirements.txt -o requirements.txt ; fi"

FROM python:3.12 AS build-stage
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
