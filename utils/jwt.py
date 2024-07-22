from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from jose import ExpiredSignatureError, jwt
from ninja.errors import HttpError
from ninja.security import HttpBearer

from apps.users.models import User
from setup import settings


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = jwt.decode(token, settings.SECRET_KEY)
            request.user = user
            return True
        except ExpiredSignatureError as exception:
            raise HttpError(HTTPStatus.UNAUTHORIZED, str(exception)) from exception
        except Exception:  # pylint: disable=broad-exception-caught
            return False


def generate_jwt_token(user: User, expiration_time_in_minutes: int = 600):
    secret_key = settings.SECRET_KEY

    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_time_in_minutes)

    payload = {
        "user_id": str(user.id),
        "exp": expiration_time,
        "name": user.name,
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_jwt_token(token: str):
    secret_key = settings.SECRET_KEY
    if "Bearer" in token:
        token = token.split(" ")[1]
    return jwt.decode(token, secret_key, algorithms=["HS256"])
