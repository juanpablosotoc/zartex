from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import AddressCreate, AddressRead
from myOrm.models import Address as AddressModel, Client
from myOrm.database import get_db_session
from myDependencies.auth import validate_is_authenticated

router = APIRouter(
    prefix="/api/v1/users/addresses",
    tags=["addresses"],
)

@router.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(
    addr_in: AddressCreate,
    db: AsyncSession = Depends(get_db_session),
    client: Client = Depends(validate_is_authenticated),
):
    # 1) Verify client exists
    result = await db.execute(select(Client).where(Client.id == client.id))
    client = result.scalars().one_or_none()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    # 2) Create address tied to that client
    new_addr = AddressModel(**addr_in.dict(), client_id=client.id)
    db.add(new_addr)
    await db.commit()
    await db.refresh(new_addr)

    return new_addr

@router.get("/", response_model=list[AddressRead])
async def list_addresses(
    db: AsyncSession = Depends(get_db_session),
    client: Client = Depends(validate_is_authenticated),
):
    result = await db.execute(
        select(AddressModel).where(AddressModel.client_id == client.id)
    )
    addresses = result.scalars().all()
    return addresses

@router.get("/{address_id}", response_model=AddressRead)
async def get_address(
    address_id: int,
    db: AsyncSession = Depends(get_db_session),
    client: Client = Depends(validate_is_authenticated),
):
    result = await db.execute(
        select(AddressModel).where(
            AddressModel.id == address_id,
            AddressModel.client_id == client.id
        )
    )
    address = result.scalars().one_or_none()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    db: AsyncSession = Depends(get_db_session),
    client: Client = Depends(validate_is_authenticated),
):
    result = await db.execute(
        select(AddressModel).where(
            AddressModel.id == address_id,
            AddressModel.client_id == client.id
        )
    )
    address = result.scalars().one_or_none()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    await db.delete(address)
    await db.commit()
