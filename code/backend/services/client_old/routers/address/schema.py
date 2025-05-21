from pydantic import BaseModel
from datetime import datetime


class AddressBase(BaseModel):
    street_address: str
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    client_id: int
    created_at: datetime

    class Config:
        from_attributes = True
