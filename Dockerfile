# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:latest

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first

# RUN apt-get update -y
# RUN apt-get install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt-get update -y
# RUN apt-get install python3.12 -y

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /backend

# Set the working directory to /music_service
WORKDIR /backend

# Copy the current directory contents into the container at /music_service
COPY authentication /backend/authentication
COPY backend /backend/backend
COPY feed /backend/feed
COPY templates /backend/templates
COPY manage.py /backend/manage.py
COPY requirements.txt /backend/requirements.txt
COPY .env /backend/.env

RUN python3 -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt