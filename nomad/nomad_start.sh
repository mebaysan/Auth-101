#! /bin/bash

# Start the Nomad agent
# sudo nomad agent -dev -bind 0.0.0.0

# Start auth service
nomad job run auth101-auth.nomad
echo "####################+AUTH service started+####################"

# Start gateway service
nomad job run auth101-gateway.nomad
echo "####################+GATEWAY service started+####################"


# Commands
# libs
#sudo apt-get install python3-httpx

# login post request
#httpx -m POST --auth user@user.com Passw0rd http://172.17.0.3:8080/login

# GET Posts
#httpx -m GET -h "Authorization" "Bearer <TOKEN>" http://172.17.0.3:8080/posts

# POST Posts
#httpx -m POST -h "Authorization" "Bearer <TOKEN>" -j '{"id":1, "title": "Title Text"}' http://172.17.0.3:8080/posts