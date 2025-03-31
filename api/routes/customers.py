# api/routes/customers.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/customers", tags=["Customers"])

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str

@router.post("/add")
def add_customer(customer: Customer):
    # Placeholder - her ville du gemme kunden i database eller fil
    return {"message": f"Kunde {customer.name} tilføjet", "customer": customer}

@router.get("/all")
def get_all_customers():
    # Dummy response
    return [{"customer_id": "cust_001", "name": "Test Firma", "email": "test@firma.dk"}]