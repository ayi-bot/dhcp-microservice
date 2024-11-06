from fastapi import Depends
from sqlmodel import Session
from app.config.db_config import engine
from app.repository.dhcp_repository import DhcpRepository


def get_session() -> Session:
    with Session(engine) as session:
        yield session


def get_dhcp_repository(db: Session = Depends(get_session)) -> DhcpRepository:
    return DhcpRepository(session=db)        