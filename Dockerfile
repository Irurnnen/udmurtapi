FROM python:3.11

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./bootstrap.sh /code/bootstrap.sh
COPY ./bootstrap.py /code/bootstrap.py
COPY ./data/init.sql /code/data/init.sql

