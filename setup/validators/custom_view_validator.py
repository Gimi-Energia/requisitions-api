from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomErrorHandlerMixin:
    def handle_validation_error(self, ve):
        errors = []
        for field, messages in ve.detail.items():
            if isinstance(messages, list):
                for message in messages:
                    if isinstance(message, dict):
                        message = "; ".join(f"{k}: {v}" for k, v in message.items())
                    errors.append(
                        f"o campo '{field}' é obrigatório"
                        if "obrigatório" in message.lower()
                        else f"No campo '{field}' {message.lower()}"
                    )
            else:
                if isinstance(messages, dict):
                    messages = "; ".join(f"{k}: {v}" for k, v in messages.items())
                errors.append(
                    f"o campo '{field}' é obrigatório"
                    if "obrigatório" in messages.lower()
                    else f"No campo '{field}' {messages.lower()}"
                )
        error_message = "; ".join(errors)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def handle_generic_exception(self, exc, request):
        exception = APIException(detail=str(exc))
        exception.status_code = status.HTTP_400_BAD_REQUEST
        response = exception_handler(exception, context={"request": request})

        if response is None:
            response = Response(
                {"detail": "Unhandled error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response
