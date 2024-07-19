import uuid

from ninja import Router

from apps.products.schema import ProductSchema, ProductSchemaInput, ProductSchemaList
from apps.products.services import ProductService
from utils.jwt import JWTAuth, decode_jwt_token

products_router = Router(auth=JWTAuth())

service = ProductService()


@products_router.post("/", response=ProductSchema)
def create_product(request, payload: ProductSchemaInput):
    """cria um produto"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.create(payload)


@products_router.get("/", response=ProductSchemaList)
def list_products(
    request,
    code: str = None,
    description: str = None,
    un: str = None,
    offset_min: int = 0,
    offset_max: int = 100,
    orderby="code",
):
    """lista todos os produtos"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list(**request.GET.dict())

@products_router.get("/sync/", response=str)
def sync_iapp(request):
    """
    Sincroniza os produtos da Iniciativa Aplicativos com o banco de dados.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        str: Uma mensagem indicando o sucesso da operação.
    """
    decode_jwt_token(request.headers.get("Authorization"))
    return service.sync_iapp()

@products_router.patch("/{product_id}/", response=ProductSchema)
def update_product(request, product_id: uuid.UUID, payload: ProductSchemaInput):
    """atualiza um produto"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.update(product_id, payload)

@products_router.delete("/{product_id}/", response=str)
def delete_product(request, product_id: uuid.UUID):
    """deleta um produto"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.delete(product_id)

@products_router.get("/{product_id}/", response=ProductSchema)
def get_product(request, product_id: uuid.UUID):
    """
    Retorna um produto com base no ID fornecido.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        product_id (uuid.UUID): O ID do produto a ser retornado.

    Returns:
        Produto: O produto correspondente ao ID fornecido.
    """
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get(product_id=product_id)

