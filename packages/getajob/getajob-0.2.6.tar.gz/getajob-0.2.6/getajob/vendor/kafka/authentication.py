from datetime import datetime, timedelta
import jwt
from .exceptions import ExpiredTokenException, InvalidTokenException


def generate_kafka_jwt(
    kafka_username: str,
    kafka_jwt_secret: str,
    expire_datetime: datetime = (datetime.utcnow() + timedelta(seconds=60)),
):
    payload = {"iss": kafka_username, "iat": datetime.utcnow(), "exp": expire_datetime}
    return jwt.encode(payload, kafka_jwt_secret, algorithm="HS256")


def decode_kafka_jwt(token: str, kafka_jwt_secret: str):
    try:
        return jwt.decode(token, kafka_jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()
