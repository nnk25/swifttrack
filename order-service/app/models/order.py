from sqlalchemy import Column, String, DateTime, func
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    client_id = Column(String)
    status = Column(String)
    pickup_address = Column(String)
    delivery_address = Column(String)
    driver_id = Column(String)
    route_id = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, server_default=func.now())
