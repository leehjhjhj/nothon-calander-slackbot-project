FROM python:3.9.6

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install vim apt-utils && apt-get clean
RUN mkdir /project
ADD . /project

WORKDIR /project

RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
EXPOSE 8000
ENTRYPOINT [ "poetry" ,"run", "uvicorn", "main:app", "--host", "0.0.0.0" ]
