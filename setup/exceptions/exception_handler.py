from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Http404):
            msg = "Recurso não encontrado."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, DjangoPermissionDenied):
            msg = "Permissão negada."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_403_FORBIDDEN)
        elif isinstance(exc, AuthenticationFailed):
            msg = "Falha na autenticação. Credenciais inválidas ou ausentes."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            msg = "Ocorreu um erro no servidor."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if "detail" not in response.data:
            formatted_errors = []
            for field, messages in response.data.items():
                string_messages = [
                    str(msg) if not isinstance(msg, str) else msg
                    for sublist in messages
                    for msg in (sublist if isinstance(sublist, list) else [sublist])
                ]
                formatted_errors.append(f"{field}: {' '.join(string_messages)}")
            data = {"error": formatted_errors}
        else:
            data = {
                "error": str(
                    response.data.get("detail", "Erro desconhecido. Por favor, tente novamente.")
                )
            }

        return Response(data, status=response.status_code)

    return response
