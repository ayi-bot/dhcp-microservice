from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

class MacAddressList(SQLModel, table=True):
    __tablename__ = "mac_address_lists"
    id: int | None = Field(default=None, primary_key=True)
    mac_addresses: dict = Field(sa_column=Column(JSON, nullable=False))
