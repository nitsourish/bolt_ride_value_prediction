FROM python:3.10
# FROM jupyter/scipy-notebook

COPY . /project

WORKDIR /project

RUN pip install -r /project/requirements.txt
RUN pip install gunicorn
# RUN command pip install pickle

EXPOSE $PORT
# RUN python3 /project/app.py
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
