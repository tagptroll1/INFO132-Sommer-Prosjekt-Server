import os

from functools import wraps

from flask import request


def protected(func):
    """
    Protected endpoint that only a request with a valid token can use.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = request.headers
        auth_header = headers.get("Authorization")

        try:
            token = os.environ["API_KEY"]
        except KeyError:
            # No token set, allow all
            return func(*args, **kwargs)

        if not auth_header:
            return {"message": "Forbidden"}, 403
        
        try:
            prefix, auth = auth_header.split(" ")
        except (AttributeError, ValueError) as err:
            return {"message": "Forbidden"}, 403

        if prefix != "token" or auth != token:
            return {"message": "Forbidden"}, 403

        return func(*args, **kwargs)
    return wrapper