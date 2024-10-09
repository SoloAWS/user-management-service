from fastapi import APIRouter, HTTPException, Path, Query
from ..schemas.user import CompanyCreate, CompanyResponse
import requests
from typing import List
import os

router = APIRouter(prefix="/company-management", tags=["Company"])

CRUD_SERVICE_URL = os.getenv("CRUD_SERVICE_URL", "http://192.168.68.111:8000")

def create_company_request(company: CompanyCreate):
    api_url = CRUD_SERVICE_URL
    endpoint = "/company/"
    data = company.model_dump()

    response = requests.post(api_url + endpoint, json=data)
    return response.json(), response.status_code

def get_company_request(company_id: str):
    api_url = CRUD_SERVICE_URL
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