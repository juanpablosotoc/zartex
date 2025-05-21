from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from myDependencies import validate_is_admin, validate_is_authenticated

from myOrm.models import Client
from myOrm.database import get_db_session
from .schema import UserCreate, UserUpdate, UserResponse
from myEncryption import Encryption

router = APIRouter(
    prefix="/api/v1/users/clients",
    tags=["clients"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_in: UserCreate,
    db: AsyncSession = Depends(get_db_session),
):
    # hash the incoming password
    hashed = Encryption.hash_password(client_in.password)
    new = Client(
        email=client_in.email,
        first_name=client_in.first_name,
        last_name=client_in.last_name,
        password_hash=hashed,
    )
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new

@router.get("/me", response_model=UserResponse)
async def get_me(
    user: Client = Depends(validate_is_authenticated)
):
    return user

@router.put("/me", response_model=UserResponse)
async def update_me(
    client_in: UserUpdate,
    db: AsyncSession = Depends(get_db_session),
    client: Client = Depends(validate_is_authenticated)
):
    # apply only the set fields
    for field, value in client_in.dict(exclude_unset=True).items():
        setattr(client, field, value)
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    user: Client = Depends(validate_is_authenticated),
    db: AsyncSession = Depends(get_db_session)
    ):
    await db.delete(user)
    await db.commit()

@router.get("/{client_id}", response_model=UserResponse)
async def get_client(
    client_id: int, 
    db: AsyncSession = Depends(get_db_session),
    user: Client = Depends(validate_is_admin)
    ):
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client
