FROM python:3.10
# FROM jupyter/scipy-notebook

WORKDIR /project

COPY . /project

RUN pip install -r requirement.txt
# RUN command pip install pickle

EXPOSE $PORT
CMD gunicorn --worker=4 --bind 0.0.0.0:$PORT app:app
