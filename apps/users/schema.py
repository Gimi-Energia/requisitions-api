import uuid

from ninja import Schema

from apps.departments.schema import DepartmentsBaseSchema


class UserBaseSchema(Schema):
    id: uuid.UUID
    name: str | None
    email: str | None
    type: str | None
    phone: str | None
    company: str | None
    department: DepartmentsBaseSchema | None = None


class UserOutputPurchaseSchema(Schema):
    id: uuid.UUID
    name: str | None
    email: str | None
