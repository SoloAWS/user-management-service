import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from datetime import date
import json
from app.routers.company import router, create_company_request, get_company_request, date_to_str
from app.schemas.user import CompanyCreate, CompanyResponse

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def custom_json_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class TestCompanyManagement(unittest.TestCase):

    @patch('requests.post')
    def test_create_company_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        company_data = CompanyCreate(
            username="testuser@example.com",
            password="testpass",
            name="Test Company",
            first_name="John",
            last_name="Doe",
            birth_date=date(2023, 1, 1),
            phone_number="+12 345 678 9012",
            country="TestCountry",
            city="TestCity"
        )
        response = client.post("/company-management/", content=json.dumps(company_data.dict(), default=custom_json_serializer), headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Test Company")

    @patch('requests.post')
    def test_create_company_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"detail": "Error creating company"}
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        company_data = CompanyCreate(
            username="testuser@example.com",
            password="testpass",
            name="Test Company",
            first_name="John",
            last_name="Doe",
            birth_date=date(2023, 1, 1),
            phone_number="+12 345 678 9012",
            country="TestCountry",
            city="TestCity"
        )
        response = client.post("/company-management/", content=json.dumps(company_data.dict(), default=custom_json_serializer), headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": {"detail": "Error creating company"}})

    @patch('requests.get')
    def test_get_company_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = client.get("/company-management/12345678-1234-5678-1234-567812345678")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Company")

    @patch('requests.get')
    def test_get_company_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"detail": "Company not found"}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = client.get("/company-management/12345678-1234-5678-1234-567812345678")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": {"detail": "Company not found"}})

    def test_get_company_invalid_id(self):
        response = client.get("/company-management/invalid-id")
        self.assertEqual(response.status_code, 422)

    def test_date_to_str(self):
        test_date = date(2023, 1, 1)
        self.assertEqual(date_to_str(test_date), "2023-01-01")

        with self.assertRaises(TypeError):
            date_to_str("not a date")

    @patch('requests.post')
    def test_create_company_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        company = CompanyCreate(
            username="testuser@example.com",
            password="testpass",
            name="Test Company",
            first_name="John",
            last_name="Doe",
            birth_date=date(2023, 1, 1),
            phone_number="+12 345 678 9012",
            country="TestCountry",
            city="TestCity"
        )

        response_data, status_code = create_company_request(company)
        self.assertEqual(status_code, 201)
        self.assertEqual(response_data["name"], "Test Company")

    @patch('requests.get')
    def test_get_company_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "12345678-1234-5678-1234-567812345678",
            "username": "testuser@example.com",
            "name": "Test Company",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "2023-01-01",
            "phone_number": "+12 345 678 9012",
            "country": "TestCountry",
            "city": "TestCity"
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response_data, status_code = get_company_request("12345678-1234-5678-1234-567812345678")
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data["name"], "Test Company")