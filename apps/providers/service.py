from http import HTTPStatus

from django.http import JsonResponse
from ninja.errors import HttpError

from apps.providers.models import Provider, Transporter
from apps.providers.schema import ProvidersBaseSchema


class TransporterService:
    def get_all_transporters(self):
        return Transporter.objects.all()

    def get_transporter_by_id(self, transporter_id: str):
        return Transporter.objects.filter(id=transporter_id).first()

    def get_transporter_by_name(self, name: str):
        return Transporter.objects.filter(name=name).first()

    def list(self):
        transporters = self.get_all_transporters()
        total = transporters.count()
        data = {"total": total, "data": transporters}
        return data

    def get(self, transporter_id: str):
        if not (transporter := self.get_transporter_by_id(transporter_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Transporter not found")
        return transporter

    def create(self, input_data: ProvidersBaseSchema):
        if self.get_transporter_by_name(input_data.name):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Transporter already exists")
        transporter = Transporter.objects.create(**input_data.dict())
        return transporter

    def update(self, transporter_id: str, input_data: ProvidersBaseSchema):
        if not (transporter := self.get_transporter_by_id(transporter_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Transporter not found")
        for attr, value in input_data.model_dump(exclude_defaults=True, exclude_unset=True).items():
            setattr(transporter, attr, value)
        transporter.save()
        transporter.refresh_from_db()
        return transporter

    def delete(self, transporter_id: str):
        if not (transporter := self.get_transporter_by_id(transporter_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Transporter not found")
        transporter.delete()
        return JsonResponse({"message": "Transporter deleted successfully"})


class ProviderService:
    def get_all_providers(self):
        return Provider.objects.all()

    def get_provider_by_id(self, provider_id: str):
        return Provider.objects.filter(id=provider_id).first()

    def get_provider_by_name(self, name: str):
        return Provider.objects.filter(name=name).first()

    def list(self):
        providers = self.get_all_providers()
        total = providers.count()
        data = {"total": total, "data": providers}
        return data

    def get(self, provider_id: str):
        if not (provider := self.get_provider_by_id(provider_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Provider not found")
        return provider

    def create(self, input_data: ProvidersBaseSchema):
        if self.get_provider_by_name(input_data.name):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Provider already exists")
        provider = Provider.objects.create(**input_data.dict())
        return provider

    def update(self, provider_id: str, input_data: ProvidersBaseSchema):
        if not (provider := self.get_provider_by_id(provider_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Provider not found")
        for attr, value in input_data.model_dump(exclude_defaults=True, exclude_unset=True).items():
            setattr(provider, attr, value)
        provider.save()
        provider.refresh_from_db()
        return provider

    def delete(self, provider_id: str):
        if not (provider := self.get_provider_by_id(provider_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Provider not found")
        provider.delete()
        return JsonResponse({"message": "Provider deleted successfully"})
