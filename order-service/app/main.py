from fastapi import FastAPI
from app.api.routes import router
from app.core.database import engine
from app.core.database import Base

app = FastAPI(title="Order Service")

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api/v1")