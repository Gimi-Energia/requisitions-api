from ninja import Schema
import uuid

class LoginSchemaInput(Schema):
    email: str
    password: str


class UserOutputSchema(Schema):
    id: uuid.UUID
    email: str
    name: str
    type: str