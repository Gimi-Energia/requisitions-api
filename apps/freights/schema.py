import uuid
from ninja import Schema
from datetime import date, datetime

class QuotationBaseSchema(Schema):
    transporter_id: uuid.UUID | None = None
    price: str | None = None
    status: str | None = None
    
class FreightsBaseSchema(Schema):
    approver: uuid.UUID
    company: str
    contract: str
    department: str
    is_internal: bool
    motive: str
    obs: str
    quotations: list[QuotationBaseSchema] | None = None
    request_date: date
    requester: uuid.UUID
    status: str

class FreigthsOutputSchema(FreightsBaseSchema):
    id: uuid.UUID
    created_at: datetime
    motive_denied: str | None = ''
    due_date: datetime | None = None
    is_internal: bool = False
    cte_number: str | None = ''