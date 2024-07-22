from http import HTTPStatus

from ninja.errors import HttpError
from django.http import JsonResponse

from apps.departments.models import Department
from apps.departments.schema import DepartmentsBaseSchema


class DepartmentService:
    def get_all_departments(self):
        return Department.objects.all()

    def get_department_by_id(self, department_id: str):
        return Department.objects.filter(id=department_id).first()

    def get_department_by_name(self, name: str):
        return Department.objects.filter(name=name).first()

    def list(self, **kwargs):
        departments = self.get_all_departments()
        total = departments.count()
        data = {"total": total, "departments": departments}

        return data

    def get(self, department_id: str):
        if not (department := self.get_department_by_id(department_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Department not found")
        return department

    def create(self, input_data: DepartmentsBaseSchema):
        if self.get_department_by_name(input_data.name):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Department already exists")

        department = Department.objects.create(**input_data.dict())
        return department

    def update(self, department_id: str, input_data: DepartmentsBaseSchema):
        if not (department := self.get_department_by_id(department_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Department not found")

        for attr, value in input_data.model_dump(exclude_defaults=True, exclude_unset=True).items():
            print(attr, value)
            setattr(department, attr, value)

        department.save()
        department.refresh_from_db()

        return department

    def delete(self, department_id: str):
        if not (department := self.get_department_by_id(department_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Department not found")

        department.delete()

        return JsonResponse({"message": "Department deleted successfully"})
