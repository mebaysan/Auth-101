"""Basic gateway service playground

# libs
- !pip install httpx pyjwt flask

# login post request
- httpx -m POST --auth user@user.com Passw0rd http://127.0.0.1:8080/login

# GET Posts
- httpx -m GET -h "Authorization" "Bearer <TOKEN>" http://127.0.0.1:8080/posts

# POST Posts
- httpx -m POST -h "Authorization" "Bearer <TOKEN>" -j '{"id":1, "title": "Title Text"}' http://127.0.0.1:8080/posts
"""
from flask import Flask, request
import httpx
import json
import os

AUTH_SERVICE_URL = (
    "http://127.0.0.1:5000"
    if os.environ.get("AUTH_SERVICE_URL", None) is None
    else os.environ.get("AUTH_SERVICE_URL")
)  # in container it will be set in ENV

POSTS_DB = []  # to simulate inserting

app = Flask(__name__)


def auth_service_validate_token(request):
    """Token validation in auth service

    Args:
        request (request): Flask request

    Returns:
        tuple: First item of the tuple will be the decoded token if the request is successfull and 2nd item will be the status code
    """
    if not "Authorization" in request.headers:
        # if there is no "Authorization" header in the request that is coming to "gateway" service, return error
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]  # token has to use the Bearer scheme!

    if not token:
        # if there is no JWT token return error
        return None, ("missing credentials", 401)

    # post request to auth service to validate the token
    response = httpx.post(
        f"{AUTH_SERVICE_URL}/validate",
        headers={"Authorization": token},
    )

    # auth service returns us the token and status code
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def auth_service_login(request):
    """Auth request to auth service

    Args:
        request (request): Flask request

    Returns:
        tuple: First item of the tuple will be the token if the request is successfull and 2nd item will be the status code
    """
    auth = request.authorization
    if not auth:
        #  if there is no "Authorization" header in the request that is coming to "gateway" service, return error
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    # post request to auth service to get the token
    response = httpx.post(f"{AUTH_SERVICE_URL}/login", auth=basicAuth)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


@app.route("/login", methods=["POST"])
def login():
    # get the token by using gateway service (we can think that the request will be redirected to the auth service)
    token, err = auth_service_login(request)
    if not err:
        return token
    else:
        return err


@app.route("/posts", methods=["POST"])
def post_posts():
    # firstly validate the token by using gateway service. By doing that we enforce to make the user to be logged in
    token, err = auth_service_validate_token(request)
    if err:
        return err
    else:
        POSTS_DB.append(request.json)
        return {"msg": "success", "data": request.json}


@app.route("/posts", methods=["GET"])
def get_posts():
    # firstly validate the token by using gateway service. By doing that we enforce to make the user to be logged in
    token, err = auth_service_validate_token(request)
    if err:
        return err

    token = json.loads(token)  # we get decoded token

    return {"posts": POSTS_DB}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=os.environ.get("DEBUG"))
