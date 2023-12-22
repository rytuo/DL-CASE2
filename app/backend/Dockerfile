FROM python:3.9

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml .
COPY poetry.lock .

COPY ../data .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./ /app