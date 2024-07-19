import uuid
from datetime import datetime, date
from apps.users.schema import UserOutputPurchaseSchema
from apps.departments.schema import DepartmentsBaseSchema
from apps.products.schema import ProductSchema
from ninja import Schema


class PurchaseBaseSchema(Schema):
    company: str
    request_date: date
    motive: str
    obs: str
    status: str
    has_quotation: bool
    control_number: int
    approval_date: datetime | None = None
    quotation_emails: str | None = None
    quotation_date: datetime | None = None


class PurchaseProductBaseSchema(Schema):
    quantity: float
    price: float | None = 0.0
    status: str


class PurchaseProductOutputSchema(ProductSchema, PurchaseProductBaseSchema):
    pass


class PurchaseProductInputSchema(PurchaseProductBaseSchema):
    product_id: uuid.UUID


class PurchaseOuputSchema(PurchaseBaseSchema):
    id: uuid.UUID
    approver: UserOutputPurchaseSchema
    requester: UserOutputPurchaseSchema
    department: DepartmentsBaseSchema
    products: list[PurchaseProductOutputSchema]
    created_at: datetime


class PurchaseInputCreateSchema(PurchaseBaseSchema):
    department_id: str
    requester_id: uuid.UUID
    approver_id: uuid.UUID
    products: list[PurchaseProductInputSchema]
