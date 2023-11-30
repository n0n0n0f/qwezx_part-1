FROM python:latest
COPY . /app
WORKDIR /app
RUN pip3 install django Pillow
CMD python manage.py runserver 127.0.0.1:8000