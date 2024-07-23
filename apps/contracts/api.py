import uuid

from ninja import Router

from apps.contracts.schema import ContractSchema, ContractSchemaList
from apps.contracts.services.contract_service import ContractService
from utils.jwt import JWTAuth, decode_jwt_token

contracts_router = Router(auth=JWTAuth())

service = ContractService()


@contracts_router.post("/", response=ContractSchema)
def create_contract(request, payload: ContractSchema):
    """Cria um contrato"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.create(payload)


@contracts_router.get("/", response=ContractSchemaList)
def list_contracts(
    request,
    company: str = None,
    offset_min: int = 0,
    offset_max: int = 100,
    orderby="contract_number",
):
    """Lista todos os contratos"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list(**request.GET.dict())


@contracts_router.get("/sync/", response=str)
def sync_iapp(request, company):
    """
    Sincroniza os contratos da Iniciativa Aplicativos com o banco de dados.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        str: Uma mensagem indicando o sucesso da operação.
    """
    decode_jwt_token(request.headers.get("Authorization"))
    return service.sync_iapp()


@contracts_router.patch("/{contract_id}/", response=ContractSchema)
def update_contract(request, contract_id: uuid.UUID, payload: ContractSchema):
    """Atualiza um contrato"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.update(contract_id, payload)


@contracts_router.delete("/{contract_id}/", response=str)
def delete_contract(request, contract_id: uuid.UUID):
    """Deleta um contrato"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.delete(contract_id)


@contracts_router.get("/{contract_id}/", response=ContractSchema)
def get_contract(request, contract_id: uuid.UUID):
    """
    Retorna um contrato com base no ID fornecido.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        contract_id (uuid.UUID): O ID do contrato a ser retornado.

    Returns:
        Contrato: O contrato correspondente ao ID fornecido.
    """
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get(contract_id=contract_id)
