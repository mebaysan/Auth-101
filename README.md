# Introduction

Nowadays, I am eager to learn microservices architecture and technologies. I was super wondering that how to handle authentication between different systems? In this repo, I experienced that in the easiest way.

Also, you can check [my text I published on Medium](https://mebaysan.medium.com/jwt-auth-101-e78aeef640c) that I wrote to explain this code.

![Worst Diagram](assets/worst-diagram.png)

# Containers & Images

## Auth Service

[auth101-auth](https://hub.docker.com/repository/docker/mebaysan/auth101-auth)

```bash
docker pull mebaysan/auth101-auth

docker container run -d -p 5000:5000 mebaysan/auth101-auth
```

## Gateway Service

[auth101-gateway](https://hub.docker.com/repository/docker/mebaysan/auth101-gateway)

```bash
docker pull mebaysan/auth101-gateway

docker container run -d -p 8080:8080 mebaysan/auth101-gateway
```