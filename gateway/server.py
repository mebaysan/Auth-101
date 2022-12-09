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

AUTH_SERVICE_URL = "http://127.0.0.1:5000"  # you should get this by using ENV
POSTS_DB = []  # to simulate inserting

app = Flask(__name__)


def auth_service_validate_token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    response = httpx.post(
        f"{AUTH_SERVICE_URL}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def auth_service_login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    response = httpx.post(f"{AUTH_SERVICE_URL}/login", auth=basicAuth)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


@app.route("/login", methods=["POST"])
def login():
    token, err = auth_service_login(request)
    if not err:
        return token
    else:
        return err


@app.route("/posts", methods=["POST"])
def post_posts():
    POSTS_DB.append(request.json)
    return {"msg": "success", "data": request.json}


@app.route("/posts", methods=["GET"])
def get_posts():
    token, err = auth_service_validate_token(request)
    if err:
        return err

    token = json.loads(token)  # we get decoded token

    return {"posts": POSTS_DB}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
