from sqlalchemy.orm import Session
from app.models.MacAddressesList import MacAddressList

class DhcpRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_mac_address_list(self, mac_addresses: list):
        db_mac_list = MacAddressList(mac_addresses=mac_addresses)
        self.session.add(db_mac_list)
        self.session.commit()
        self.session.refresh(db_mac_list)
        return db_mac_list

    def get_latest_mac_address_list(self):
        return self.session.query(MacAddressList).order_by(MacAddressList.id.desc()).first()
