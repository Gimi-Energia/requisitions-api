import uuid
from datetime import date, datetime

from ninja import Schema

from apps.departments.schema import DepartmentsBaseSchema
from apps.products.schema import ProductSchema
from apps.users.schema import UserOutputPurchaseSchema


class PurchaseBaseSchema(Schema):
    company: str  | None = None
    request_date: date | None = None
    motive: str | None = None
    obs: str | None = None
    status: str | None = None
    has_quotation: bool | None = None
    control_number: int | None = None
    approval_date: datetime | None = None
    quotation_emails: str | None = None
    quotation_date: datetime | None = None


class PurchaseProductBaseSchema(Schema):
    quantity: float | None = None
    price: float | None = 0.0
    status: str | None = None


class PurchaseProductOutputSchema(ProductSchema, PurchaseProductBaseSchema):
    pass


class PurchaseProductInputSchema(PurchaseProductBaseSchema):
    product_id: uuid.UUID


class PurchaseOutputSchema(PurchaseBaseSchema):
    id: uuid.UUID
    approver: UserOutputPurchaseSchema
    requester: UserOutputPurchaseSchema
    department: DepartmentsBaseSchema
    products: list[PurchaseProductOutputSchema]
    created_at: datetime


class PurchaseInputCreateSchema(PurchaseBaseSchema):
    department_id: str | None = None
    requester_id: uuid.UUID
    approver_id: uuid.UUID
    products: list[PurchaseProductInputSchema]


class PurchaseInputUpdateSchema(PurchaseBaseSchema):
    department_id: str | None = None
    requester_id: uuid.UUID | None = None
    approver_id: uuid.UUID | None = None
