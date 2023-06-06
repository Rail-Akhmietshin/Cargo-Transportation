FROM python:3.11

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y netcat alembic gunicorn
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir /WelbeX

WORKDIR /WelbeX

COPY pyproject.toml .
COPY poetry.lock .

RUN pip3 install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /WelbeX

ENV PYTHONPATH=/WelbeX

RUN chmod a+x docker/*.sh

#CMD  ["/WelbeX/docker/app.sh"]