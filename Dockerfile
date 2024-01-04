FROM python:3.10.7

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1  # dont create .pyc files
ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade
RUN pip install --upgrade pip
RUN useradd -rms /bin/bash djdjdj
WORKDIR /poputka
COPY --chown=djdjdj:djdjdj . .
RUN pip install -r requirements.txt
USER djdjdj
