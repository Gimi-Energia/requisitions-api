from ninja import Schema


class LoginSchemaInput(Schema):
    email: str
    password: str
