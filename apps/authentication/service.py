import uuid
from http import HTTPStatus

from django.contrib.auth import authenticate
from django.http import JsonResponse
from ninja.errors import HttpError

from apps.authentication.schema import LoginSchemaInput
from apps.users.models import User
# from communication.mailing.service import send_email
from utils.jwt import generate_jwt_token

# from sentry_sdk import set_user as set_user_sentry


class AuthenticationService:
    def auth_login(self, request, input_schema: LoginSchemaInput):
        if not (
            user := authenticate(request, email=input_schema.email, password=input_schema.password)
        ):
            return JsonResponse({"error": "Invalid credentials"}, status=HTTPStatus.UNAUTHORIZED)
        token = generate_jwt_token(user=user)
        return JsonResponse(
            data={"access_token": token},
            status=HTTPStatus.OK,
        )

    def get_me(self, user_id: uuid.UUID):
        if not (user := User.objects.filter(id=user_id).first()):
            raise HttpError(HTTPStatus.NOT_FOUND, "User not found")
        return user
