from typing import Annotated, List, Union
from fastapi import APIRouter, Depends
from app.dependencies import get_dhcp_repository
from app.repository.dhcp_repository import DhcpRepository
from app.routeros_api import RouterOsApiPool
import os
from dotenv import load_dotenv

load_dotenv()

dhcp_router = APIRouter()

@dhcp_router.get("/save_mac_addresses", response_model=List[str])
def save(service: Annotated[DhcpRepository, Depends(get_dhcp_repository)]):
    api_pool = RouterOsApiPool(
        os.getenv("ROUTER_IP"),
        username=os.getenv("ROUTER_USERNAME"),
        password=os.getenv("ROUTER_PASSWORD"),
        port=int(os.getenv("ROUTER_PORT")),
        plaintext_login=False,
        use_ssl=False
    )
    api = api_pool.get_api()

    try:
        leases = api.get_resource('/ip/dhcp-server/lease')
        raw_lease_data = leases.call('print') 
        response_data = []

        for lease in raw_lease_data:
            if 'active-address' in lease:
                try:
                    mac_address = lease.get('mac-address', '')
                    response_data.append(mac_address)
                except UnicodeDecodeError as e:
                    print(f"Decoding error in lease data: {e}")
                    response_data.append({"Error": "Decoding error encountered in one of the lease entries."})

        service.save_mac_address_list(response_data)

        return response_data

    finally:
        api_pool.disconnect()


@dhcp_router.get("/latest_mac_addresses", response_model=Union[List[str], dict])
def get_latest(service: Annotated[DhcpRepository, Depends(get_dhcp_repository)]):
    latest_mac_list = service.get_latest_mac_address_list()
    
    if latest_mac_list and latest_mac_list.mac_addresses:
        return latest_mac_list.mac_addresses
    else:
        return {"message": "No MAC addresses found."}        
