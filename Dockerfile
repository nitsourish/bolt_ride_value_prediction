FROM python:3.10
# FROM jupyter/scipy-notebook

COPY . /project

WORKDIR /project

RUN pip install -r /project/requirements.txt
# RUN command pip install pickle

EXPOSE $PORT
CMD gunicorn --worker=4 --bind 0.0.0.0:$PORT app:app
