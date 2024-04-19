from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Http404):
            msg = "Recurso não encontrado."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, ObjectDoesNotExist):
            msg = "O objeto solicitado não foi encontrado."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, ValidationError):
            errors = set()
            for field, messages in exc.detail.items():
                if isinstance(messages, list):
                    for message in messages:
                        errors.add(f"{field}: {str(message)}")
                else:
                    errors.add(f"{field}: {str(messages)}")
            msg = "Dados inválidos: " + "; ".join(errors)
            data = {"error": msg}
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, ParseError):
            msg = "Erro de análise: Dados malformados."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, NotAuthenticated):
            msg = "Não autenticado: Credenciais não fornecidas."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_401_UNAUTHORIZED)
        elif isinstance(exc, PermissionDenied):
            msg = "Permissão negada: Acesso não autorizado."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_403_FORBIDDEN)
        elif isinstance(exc, MethodNotAllowed):
            msg = "Método não permitido: Use " + str(exc.detail)
            data = {"error": msg}
            response = Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif isinstance(exc, Throttled):
            msg = f"Limite de requisições atingido. Tente novamente em {exc.wait} segundos."
            data = {"error": msg}
            response = Response(data, status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            data = {"error": "Ocorreu um erro no servidor."}
            response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if isinstance(response.data, dict) and "detail" in response.data:
            if isinstance(response.data["detail"], dict):
                errors = set()
                for field, content in response.data["detail"].items():
                    if isinstance(content, list):
                        for error in content:
                            errors.add(f"{field}: {str(error)}")
                    else:
                        errors.add(f"{field}: {str(content)}")
                data = {"error": "; ".join(errors)}
            else:
                data = {"error": str(response.data["detail"])}
        else:
            errors = set()
            for field, content in response.data.items():
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and "non_field_errors" in item:
                            errors.update(item["non_field_errors"])
                        elif isinstance(item, dict):
                            for key, value in item.items():
                                if isinstance(value, list):
                                    errors.add(f"{key}: {' '.join(str(v) for v in value)}")
                                else:
                                    errors.add(f"{key}: {str(value)}")
                        else:
                            errors.add(str(item))
                else:
                    errors.add(f"{field}: {str(content)}")
            data = {"error": "; ".join(errors)}

        response = Response(data, status=response.status_code)

    return response
