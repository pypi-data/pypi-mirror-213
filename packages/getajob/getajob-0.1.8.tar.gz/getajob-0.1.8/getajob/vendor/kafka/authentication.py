import jwt
from datetime import datetime, timedelta

from getajob.config.settings import SETTINGS
from .exceptions import ExpiredTokenException, InvalidTokenException


def generate_kafka_jwt():
    payload = {
        "iss": SETTINGS.KAFKA_USERNAME,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=60),
    }
    return jwt.encode(payload, SETTINGS.KAFKA_JWT_SECRET, algorithm="HS256")


def decode_kafka_jwt(token: str) -> None:
    try:
        return jwt.decode(token, SETTINGS.KAFKA_JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()
