import uuid

from ninja import Schema


class ProvidersBaseSchema(Schema):
    name: str | None = None
    cnpj: str | None = None
    email: str | None = None
    phone: str | None = None


class ProvidersOutputSchema(ProvidersBaseSchema):
    id: uuid.UUID


class ProvidersSchemaList(Schema):
    total: int = 0
    data: list[ProvidersOutputSchema] | None = []
