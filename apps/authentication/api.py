from ninja import Router

from apps.authentication.schema import LoginSchemaInput
from apps.authentication.service import AuthenticationService
from utils.jwt import JWTAuth, decode_jwt_token

authentication_router = Router(auth=None)

service = AuthenticationService()


@authentication_router.post("/login/")
def auth_login(request, input_schema: LoginSchemaInput):
    """Autenticação de usuário"""
    return service.auth_login(request, input_schema)
