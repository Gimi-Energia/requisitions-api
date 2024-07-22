from ninja import Schema


class DepartmentsBaseSchema(Schema):
    id: str | None = None
    name: str | None = None


class DepartmentsSchemaList(Schema):
    total: int = 0
    departments: list[DepartmentsBaseSchema] = []
