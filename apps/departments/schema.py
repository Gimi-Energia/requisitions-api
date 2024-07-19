from ninja import Schema


class DepartmentsBaseSchema(Schema):
    id: str | None
    name: str | None
