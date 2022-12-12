FROM python:3.11-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV DEBUG=True

ENV JWT_SECRET=this-is-so-secret-key-to-encode-jwt-tokens

EXPOSE 5000

ENTRYPOINT [ "python", "server.py" ]