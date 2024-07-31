import uuid
from apps.freights.schema import FreightsBaseSchema, QuotationBaseSchema, FreigthsOutputSchema
from apps.freights.models import Freight, FreightQuotation
from apps.contracts.services.contract_service import ContractService
from apps.departments.service import DepartmentService
from ninja.errors import HttpError
from http import HTTPStatus
from datetime import datetime

class FreightService():
    
    @property
    def department_service(self):
        return DepartmentService()
    
    @property
    def contract_service(self):
        return ContractService()
    
    def __build_data(self, freight: Freight):
        data = {
            "id": freight.id,
            "company": freight.company,
            "department": freight.department.id,
            "created_at": freight.created_at,
            "request_date": freight.request_date,
            "requester": freight.requester.id,
            "motive": freight.motive,
            "obs": freight.obs,
            "status": freight.status,
            "quotations": [],
            "approver": freight.approver.id,
            "approval_date": freight.approval_date,
            "cte_number": freight.cte_number,
            "contract": freight.contract.id,
            "is_internal": freight.is_internal,
            "motive_denied": freight.motive_denied,  
            "due_date": freight.due_date      
        }
        for quotation in freight.freightquotation_set.all():
            data["quotations"].append({
                "transporter_id": quotation.transporter_id,
                "price": quotation.price,
                "status": quotation.status
            })
        return data
    def create_quotation(self, freight_id: uuid.UUID, payload: QuotationBaseSchema):
        return FreightQuotation.objects.create(freight_id=freight_id,
                                               price=float(payload.price),
                                               status=payload.status,
                                               transporter_id=payload.transporter_id)
    
    def create_freight(self, payload: FreightsBaseSchema):
        if not (contract := self.contract_service.get_contract_by_id(payload.contract)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Contract not found")
        
        if not (department := self.department_service.get_department_by_id(payload.department)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Department not found")
        
        freight = Freight.objects.create(
            company=payload.company,
            department=department,
            request_date=payload.request_date,
            requester_id=payload.requester,
            motive=payload.motive,
            obs=payload.obs,
            status=payload.status,
            approver_id=payload.approver,
            contract=contract,
            is_internal=payload.is_internal
        )
        if payload.is_internal:
            freight.approval_date = datetime.now()
            
        if payload.quotations:
            quatation_list = []
            for quotation in payload.quotations:
                quatation_list.append(self.create_quotation(freight.id, quotation).id)
                
        freight.save()
        return self.__build_data(freight)