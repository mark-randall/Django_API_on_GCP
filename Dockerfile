FROM python:3.8-slim-buster

ENV APP_HOME /app
ENV PORT 8080
ENV PYTHONUNBUFFERED 1

ADD start-up.sh /root/start-up.sh

WORKDIR $APP_HOME
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./start-up.sh && ./start-up.sh

CMD gunicorn --bind :$PORT --workers 1 --threads 8 project.wsgi:application
