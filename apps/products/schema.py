import uuid

from ninja import ModelSchema, Schema

from apps.products.models import Product


class ProductSchemaInput(Schema):
    code: str | None
    description: str | None
    un: str | None


# class ProductSchema(ModelSchema):
#     class Meta:
#         model = Product
#         fields = "__all__"


class ProductSchema(ProductSchemaInput):
    id: uuid.UUID


class ProductSchemaList(Schema):
    total: int = 0
    products: list[ProductSchema] = []
