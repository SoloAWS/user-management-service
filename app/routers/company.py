from fastapi import APIRouter, HTTPException, Path, Query
from ..schemas.user import CompanyCreate, CompanyResponse
import requests
import os
from datetime import date


router = APIRouter(prefix="/company-management", tags=["Company"])

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

def date_to_str(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def create_company_request(company: CompanyCreate):
    api_url = USER_SERVICE_URL
    endpoint = "/company/"
    data = company.model_dump()
    
    if 'birth_date' in data:
        data['birth_date'] = date_to_str(data['birth_date'])
        
    response = requests.post(api_url + endpoint, json=data)
    return response.json(), response.status_code

def get_company_request(company_id: str):
    api_url = USER_SERVICE_URL
    endpoint = f"/company/{company_id}"

    response = requests.get(api_url + endpoint)
    return response.json(), response.status_code

@router.post("/", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate):
    response_data, status_code = create_company_request(company)
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response_data)
    return response_data

@router.get("/{company_id}", response_model=CompanyResponse, status_code=200)
def get_company(
    company_id: str = Path(..., description="Id of the company", pattern="^[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}$")
):
    response_data, status_code = get_company_request(company_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response_data)
    return response_data