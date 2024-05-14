FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /backend/
# COPY authentication /backend/
# COPY backend /backend/
# COPY ecommerce /backend/
# COPY feed /backend/
# COPY templates /backend/
# COPY .env /backend/
# COPY manage.py /backend/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
