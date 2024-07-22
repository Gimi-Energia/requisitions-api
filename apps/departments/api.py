from ninja import Router

from apps.departments.schema import (DepartmentsBaseSchema,
                                     DepartmentsSchemaList)
from apps.departments.service import DepartmentService
from utils.jwt import JWTAuth, decode_jwt_token

departments_router = Router(auth=JWTAuth())

service = DepartmentService()


@departments_router.post("/", response=DepartmentsBaseSchema)
def create_department(request, payload: DepartmentsBaseSchema):
    """Cria um departamento"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.create(payload)


@departments_router.get("/", response=DepartmentsSchemaList)
def list_departments(request):
    """Lista todos os departamento"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list(**request.GET.dict())


@departments_router.patch("/{department_id}/", response=DepartmentsBaseSchema)
def update_department(request, department_id: str, payload: DepartmentsBaseSchema):
    """Atualiza um departamento"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.update(department_id, payload)


@departments_router.delete("/{department_id}/", response=str)
def delete_department(request, department_id: str):
    """Deleta um departamento"""
    decode_jwt_token(request.headers.get("Authorization"))
    return service.delete(department_id)


@departments_router.get("/{department_id}/", response=DepartmentsBaseSchema)
def get_department(request, department_id: str):
    """
    Retorna um departamento com base no ID fornecido.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        department_id (str): O ID do departamento a ser retornado.

    Returns:
        Departamento: O departamento correspondente ao ID fornecido.
    """
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get(department_id=department_id)
