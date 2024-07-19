from http import HTTPStatus

from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from jose import ExpiredSignatureError, jwt
from ninja.errors import HttpError
from ninja.security import HttpBearer

from apps.authentication.schema import LoginSchemaInput
from setup import settings

# from communication.mailing.service import send_email
from utils.jwt import generate_jwt_token

# from sentry_sdk import set_user as set_user_sentry


class AuthenticationService:
    def auth_login(self, request, input_schema: LoginSchemaInput):
        if not (user := authenticate(request, email=input_schema.email, password=input_schema.password)):
            return JsonResponse({"error": "Invalid credentials"}, status=HTTPStatus.UNAUTHORIZED)
        token = generate_jwt_token(user=user)
        return JsonResponse(
            data={"access_token": token},
            status=HTTPStatus.OK,
        )
