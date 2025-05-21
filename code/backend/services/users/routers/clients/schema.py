from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic models for request/response
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_afiliado: bool

    class Config:
        from_attributes = True

class AfiliadoCreate(BaseModel):
    cell_phone: str

class Token(BaseModel):
    access_token: str
    token_type: str
