from fastapi import FastAPI
from app.routers.dhcp import dhcp_router
from app.config.db_config import create_db_and_tables

app = FastAPI()

app.include_router(dhcp_router, prefix="/dhcp", tags=["dhcp"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Are you in API"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
