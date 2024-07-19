import uuid

from ninja import Router

from apps.purchases.schema import (
    PurchaseOuputSchema,
    PurchaseInputCreateSchema,
    PurchaseProductInputSchema,
)
from apps.purchases.services.purchases_service import PurchasesService
from utils.jwt import JWTAuth, decode_jwt_token

purchases_router = Router(auth=JWTAuth())

service = PurchasesService()


@purchases_router.post("/add/product/{purchase_id}/", response=PurchaseOuputSchema)
def add_product(request, purchase_id: uuid.UUID, payload: PurchaseProductInputSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.add_product(purchase_id, payload)


@purchases_router.delete("/delete/product/{purchase_id}/{product_id}/", response=str)
def delete_product(request, purchase_id: uuid.UUID, product_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.delete_product(purchase_id, product_id=product_id)


@purchases_router.get("/", response=list[PurchaseOuputSchema])
def list_purchases(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list()


@purchases_router.post("/", response=PurchaseOuputSchema)
def create_purchase(request, payload: PurchaseInputCreateSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.create(payload)
