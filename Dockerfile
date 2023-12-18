FROM ubuntu:latest

LABEL authors="petrovych"

ENTRYPOINT ["top", "-b"]

FROM python:3.12.0

ENV PYTHONBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY . /app
RUN pip install -e .  # install a package in "editable" mode This allows you to make changes to the code, and the changes take effect immediately without needing to reinstall the package.