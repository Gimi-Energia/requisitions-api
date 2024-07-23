import uuid

from ninja import Router

from apps.purchases.schema import (
    PurchaseInputCreateSchema,
    PurchaseInputUpdateSchema,
    PurchaseOutputSchema,
    PurchaseProductBaseSchema,
    PurchaseProductInputSchema,
)
from apps.purchases.services.purchases_service import PurchasesService
from utils.jwt import JWTAuth, decode_jwt_token

purchases_router = Router(auth=JWTAuth())

service = PurchasesService()


@purchases_router.get("/", response=list[PurchaseOutputSchema])
def list_purchases(request):
    """Lista todas as compras"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list()


@purchases_router.get("/{purchase_id}/", response=PurchaseOutputSchema)
def get_purchase(request, purchase_id: uuid.UUID):
    """
    Retorna uma compra com base no ID fornecido.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        purchase_id (uuid.UUID): O ID da compra a ser retornado.

    Returns:
        Compra: A compra correspondente ao ID fornecido.
    """
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get(purchase_id=purchase_id)


@purchases_router.post("/", response=PurchaseOutputSchema)
def create_purchase(request, payload: PurchaseInputCreateSchema):
    """Cria uma compra"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.create(payload)


@purchases_router.patch("/{purchase_id}/", response=PurchaseOutputSchema)
def update_purchase(request, purchase_id: uuid.UUID, payload: PurchaseInputUpdateSchema):
    """Atualiza uma compra"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.update(purchase_id, payload)


@purchases_router.delete("/{purchase_id}/", response=str)
def delete_purchase(request, purchase_id: uuid.UUID):
    """Deleta uma compra"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.delete(purchase_id)


@purchases_router.post("/add/product/{purchase_id}/", response=PurchaseOutputSchema)
def add_product(request, purchase_id: uuid.UUID, payload: PurchaseProductInputSchema):
    """Adiciona um produto em uma compra"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.add_product(purchase_id, payload)


@purchases_router.patch(
    "/update/product/{purchase_id}/{product_id}/", response=PurchaseOutputSchema
)
def update_product(
    request, purchase_id: uuid.UUID, product_id: uuid.UUID, payload: PurchaseProductBaseSchema
):
    """Atualiza um produto de uma compra"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.update_product(purchase_id, product_id, payload)


@purchases_router.delete("/delete/product/{purchase_id}/{product_id}/", response=str)
def delete_product(request, purchase_id: uuid.UUID, product_id: uuid.UUID):
    """Deleta um produto de uma compra"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.delete_product(purchase_id, product_id=product_id)
