from pydantic import BaseModel

class OrderCreate(BaseModel):
    client_id: str
    pickup_address: str
    delivery_address: str
    priority: str