from http import HTTPStatus

from django.db import transaction
from django.http import JsonResponse
from ninja.errors import HttpError

from apps.contracts.models import Contract
from apps.contracts.schema import ContractSchema
from apps.contracts.services.iapp_service import get_iapp_contracts


class ContractService:
    def get_all_contracts(self):
        return Contract.objects.all()

    def get_contract_by_id(self, contract_id: str):
        return Contract.objects.filter(id=contract_id).first()

    def list_contracts_by_list_id(self, list_id: list[str]):
        return Contract.objects.filter(id__in=list_id)

    def get_contract_by_company_and_process(self, company: str, contract_number: str):
        return Contract.objects.filter(company=company, contract_number=contract_number).first()

    def bulk_create_contract(self, list_contracts: list[Contract]):
        with transaction.atomic():
            return Contract.objects.bulk_create(list_contracts)

    def __filter_contracts(self, contracts: Contract, **kwargs):
        if company := kwargs.get("company"):
            if not contracts:
                contracts = Contract.objects.filter(company=company)
            else:
                contracts = contracts.filter(company=company)

        return contracts

    def list(self, **kwargs):
        if not kwargs.get("company"):
            contracts = self.get_all_contracts()
        else:
            contracts = self.__filter_contracts(None, **kwargs)
        orderby = kwargs.get("orderby", "code")
        contracts = contracts.order_by(orderby)
        total = contracts.count()
        offset_min = int(kwargs.get("offset_min"))
        offset_max = int(kwargs.get("offset_max"))
        data = {"total": total, "contracts": contracts[offset_min:offset_max]}
        return data

    def get(self, contract_id: str):
        if not (contract := self.get_contract_by_id(contract_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Contract not found")
        return contract

    def create(self, input_data: ContractSchema):
        if self.get_contract_by_company_and_process(input_data.company, input_data.contract_number):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Contract already exists")

        contract = Contract.objects.create(**input_data.dict())
        return contract

    def update(self, contract_id: str, input_data: ContractSchema):
        if not (contract := self.get_contract_by_id(contract_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Contract not found")

        for attr, value in input_data.model_dump(exclude_defaults=True, exclude_unset=True).items():
            print(attr, value)
            setattr(contract, attr, value)
        contract.save()
        contract.refresh_from_db()
        return contract

    def delete(self, contract_id: str):
        if not (contract := self.get_contract_by_id(contract_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Contract not found")
        contract.delete()
        return JsonResponse({"message": "Contract deleted successfully"})

    def sync_iapp(self, company: str):
        try:
            iapp_contracts = get_iapp_contracts(company)
            if not iapp_contracts:
                raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Error finding contracts")

            list_contract_exists = self.list_contracts_by_list_id(
                [iapp_contract["id"] for iapp_contract in iapp_contracts]
            )
            list_contract_exists = list_contract_exists.values_list("id", flat=True)
            list_contract_for_create = []

            for contract in iapp_contracts:
                if (
                    contract["id"] not in list_contract_exists
                    and contract["id"] not in list_contract_for_create
                ):
                    list_contract_for_create.append(Contract(**contract))

            self.bulk_create_contract(list_contract_for_create)
            return JsonResponse({"message": "Data entered successfully"})
        except Exception as e:
            raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, "Error inserting data: " + str(e))
