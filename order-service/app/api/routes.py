from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from app.schemas.order_schema import OrderCreate
from app.models.order import Order
from app.core.database import SessionLocal
from app.events.publisher import publish_event
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_id = f"ORD-{uuid.uuid4().hex[:8]}"
    print(type(order))
    new_order = Order(
        order_id=order_id,
        client_id=order.client_id,
        status="CREATED"
    )

    db.add(new_order)
    db.commit()

    await publish_event(
        "order.created",
        {
            "order_id": order_id,
            "client_id": order.client_id,
            "pickup_address": order.pickup_address,
            "delivery_address": order.delivery_address,
            "priority": order.priority
        }
    )

    return {"order_id": order_id, "status": "CREATED"}

@router.get("/orders/{order_id}")
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    return {
        "order_id": order.order_id,
        "client_id": order.client_id,
        "status": order.status
    }

@router.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    if not orders:
        return {"error": "No orders"}
    return {"orders": json.dumps(orders)}