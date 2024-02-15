import jwt, datetime
from rest_framework import exceptions


def create_access_token(id):
    return jwt.encode(
        {
            "user_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            "iat": datetime.datetime.utcnow(),
        },
        "access_secret",
        algorithm="HS256",
    ).decode("utf-8")


def decode_access_token(token):
    print("Received token:", token)
    try:
        decoded_token = jwt.decode(token, "access_secret", algorithms="HS256")
        print("Decoded token payload:", decoded_token)
        payload = jwt.decode(token, "access_secret", algorithms="HS256")
        print("user id is", payload["user_id"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError as e:
        print("Invalid token error:", e)
        raise exceptions.AuthenticationFailed("Invalid token")
    except Exception as e:
        print("Error during decoding:", e)
        raise exceptions.AuthenticationFailed("Failed to authenticate")


def create_refresh_token(id):
    return jwt.encode(
        {
            "user_id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
        },
        "refresh_secret",
        algorithm="HS256",
    )


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "refresh_secret", algorithms="HS256")

        return payload["user_id"]
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")
