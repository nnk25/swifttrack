from pydantic import BaseModel
from app.models.order import OrderStatus


class CreateOrderRequest(BaseModel):
    description: str
    destination: str


class OrderResponse(BaseModel):
    id: str
    client_id: str
    driver_id: str | None = None
    description: str
    destination: str
    status: OrderStatus
    failed_reason: str | None = None
    digital_signature_url: str | None = None
    pod_image_url: str | None = None
    created_at: str


    class Config:
        from_attributes = True
