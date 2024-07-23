from ninja import Schema


class ContractSchema(Schema):
    id: str | None = None
    company: str | None = None
    contract_number: str | None = None
    control_number: str | None = None
    client_name: str | None = None
    project_name: str | None = None
    freight_estimated: float | None = None
    freight_consumed: float | None = 0


class ContractSchemaList(Schema):
    total: int = 0
    contracts: list[ContractSchema] = []
