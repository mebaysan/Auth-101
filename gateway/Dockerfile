FROM python:3.11-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV DEBUG=True

ENV AUTH_SERVICE_URL=http://127.0.0.1:5000

EXPOSE 8080

ENTRYPOINT [ "python", "server.py" ]