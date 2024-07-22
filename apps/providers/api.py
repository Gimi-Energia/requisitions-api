from ninja import Router

from apps.providers.schema import ProvidersBaseSchema, ProvidersOutputSchema, ProvidersSchemaList
from apps.providers.service import ProviderService, TransporterService
from utils.jwt import JWTAuth, decode_jwt_token

transporters_router = Router(auth=JWTAuth())
providers_router = Router(auth=JWTAuth())

transporter_service = TransporterService()
provider_service = ProviderService()


@transporters_router.post("/", response=ProvidersOutputSchema)
def create_transporter(request, payload: ProvidersBaseSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return transporter_service.create(payload)


@transporters_router.get("/", response=ProvidersSchemaList)
def list_transporters(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return transporter_service.list()


@transporters_router.patch("/{transporter_id}/", response=ProvidersOutputSchema)
def update_transporter(request, transporter_id: str, payload: ProvidersBaseSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return transporter_service.update(transporter_id, payload)


@transporters_router.delete("/{transporter_id}/", response=str)
def delete_transporter(request, transporter_id: str):
    decode_jwt_token(request.headers.get("Authorization"))
    return transporter_service.delete(transporter_id)


@transporters_router.get("/{transporter_id}/", response=ProvidersOutputSchema)
def get_transporter(request, transporter_id: str):
    decode_jwt_token(request.headers.get("Authorization"))
    return transporter_service.get(transporter_id)


@providers_router.post("/", response=ProvidersOutputSchema)
def create_provider(request, payload: ProvidersBaseSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return provider_service.create(payload)


@providers_router.get("/", response=ProvidersSchemaList)
def list_providers(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return provider_service.list()


@providers_router.patch("/{provider_id}/", response=ProvidersOutputSchema)
def update_provider(request, provider_id: str, payload: ProvidersBaseSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return provider_service.update(provider_id, payload)


@providers_router.delete("/{provider_id}/", response=str)
def delete_provider(request, provider_id: str):
    decode_jwt_token(request.headers.get("Authorization"))
    return provider_service.delete(provider_id)


@providers_router.get("/{provider_id}/", response=ProvidersOutputSchema)
def get_provider(request, provider_id: str):
    decode_jwt_token(request.headers.get("Authorization"))
    return provider_service.get(provider_id)
