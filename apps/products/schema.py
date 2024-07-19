import uuid

from ninja import Schema


class ProductSchemaInput(Schema):
    code: str | None = None
    description: str | None = None
    un: str | None = None


class ProductSchema(ProductSchemaInput):
    id: uuid.UUID


class ProductSchemaList(Schema):
    total: int = 0
    products: list[ProductSchema] = []
