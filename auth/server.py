"""Basic authentication playground

# libs
- !pip install httpx pyjwt flask

# login post request
- httpx -m POST --auth user@user.com Passw0rd http://127.0.0.1:5000/login

# validate post request
- httpx -m POST -h "Authorization" "Bearer <TOKEN>" http://127.0.0.1:5000/validate

# HTTP headers docs
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers

# HTTP Authorization header docs
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization

# HTTP Authentication docs
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication

# Bearer Token Scientific docs
- https://www.rfc-editor.org/rfc/rfc6750.html

# HTTP response status codes
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
from flask import Flask, request
import jwt
import datetime

JWT_SECRET = (
    "this-is-so-secret-key-to-encode-jwt-tokens"  # you should get this by using ENV
)
USERS_DB = [
    {"username": "user@user.com", "password": "Passw0rd", "is_admin": True}
]  # you should use a real db :)

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    print(request.headers)  # We need to get "Authorization" header of the request
    print(request.authorization)  # This is automatically decode the header in Flask

    # handle username and password from request header (Flask does for us, it decodes)
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # filter users
    users_list = [u for u in USERS_DB if u["username"] == auth.username]
    # is there any user with the credentials
    if len(users_list) != 1 or users_list[0]["password"] != auth.password:
        return ("Missing credentials", 401)
    else:
        return createJWT(auth.username, JWT_SECRET, users_list[0]["is_admin"]), 200


@app.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers[
        "Authorization"
    ]  # handle "Authorization" header. We have to send the token in this scheme => Bearer <TOKEN>

    if not encoded_jwt:
        return ("missing credentials", 401)

    encoded_jwt = encoded_jwt.split(" ")[1]  # get the token (exclude "Bearer")

    try:
        decoded = jwt.decode(
            encoded_jwt, JWT_SECRET, algorithms=["HS256"]
        )  # decode the token
    except:
        return ("not authorized", 403)

    return (decoded, 200)


def createJWT(username, secret, authz):
    payload = {
        "username": username,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc)  # expire date
        + datetime.timedelta(days=1),  # token lifetime is 1 day
        "iat": datetime.datetime.utcnow(),  # issued at
        "admin": authz,  # is user admin
    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
    )  # return JWT token


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
