import uuid

from ninja import Router
from apps.freights.services.freights_service import FreightService
from apps.freights.schema import FreightsBaseSchema
from utils.jwt import JWTAuth, decode_jwt_token

freights_router = Router(auth=JWTAuth())

service = FreightService()

@freights_router.post('/', auth=None)
def create_freight(request, payload: FreightsBaseSchema):
    return service.create_freight(payload)