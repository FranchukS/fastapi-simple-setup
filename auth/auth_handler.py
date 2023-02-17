# This file is responsible for signing , encoding , decoding and returning JWTS
import time

import jwt

import settings


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def sign_jwt(user_email: str) -> dict[str, str]:
    payload = {
        "user_email": user_email,
        "expires": time.time() + settings.TOKEN_EXPIRED_TIME
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
