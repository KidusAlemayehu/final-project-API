FROM python:3.10-slim-buster

RUN apt-get update

RUN apt install -y libpq-dev cron redis g++ build-essential

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /CITAPI
WORKDIR /CITAPI

COPY requirements.txt /CITAPI/

COPY ./CIT_STAFF /CITAPI/

RUN pip3 install -r /CITAPI/requirements.txt

CMD ["python", "/CIT_API/manage.py", "runserver", "0.0.0.0:8888"]