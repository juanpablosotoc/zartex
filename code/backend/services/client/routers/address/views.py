# own imports
from orm import Client, Address
from .schema import AddressCreate, AddressResponse
from dependencies import validate_is_authenticated, DBSessionDep

# external imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from typing import List

# Router configuration
router = APIRouter(
    prefix="/api/v1/address",
    tags=["address"]
)

# Routes
@router.post("/address", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(
    db_session_gen: DBSessionDep,
    address: AddressCreate,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Add a new address for the current user.

    Args:
        db_session_gen: Database session dependency
        address: Address data
        user: Authenticated user from dependency

    Returns:
        AddressResponse: Created address data
    """
    db_session = await db_session_gen.__anext__()
    
    # If this is the first address, make it default
    if address.is_default:
        # Update all other addresses to non-default
        await db_session.execute(
            select(Address)
            .where(Address.client_id == user.id)
            .update({"is_default": False})
        )
    
    db_address = Address(
        client_id=user.id,
        **address.model_dump()
    )
    db_session.add(db_address)
    await db_session.commit()
    await db_session.refresh(db_address)
    return db_address

@router.get("/addresses", response_model=List[AddressResponse])
async def read_addresses(
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Get all addresses for the current user.

    Args:
        db_session_gen: Database session dependency
        user: Authenticated user from dependency

    Returns:
        List[AddressResponse]: List of user's addresses
    """
    db_session = await db_session_gen.__anext__()
    result = await db_session.execute(
        select(Address).where(Address.client_id == user.id)
    )
    return result.scalars().all()

@router.put("/address/{address_id}", response_model=AddressResponse)
async def update_address(
    db_session_gen: DBSessionDep,
    address_id: int,
    address_update: AddressCreate,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Update an existing address.

    Args:
        db_session_gen: Database session dependency
        address_id: ID of the address to update
        address_update: Updated address data
        user: Authenticated user from dependency

    Returns:
        AddressResponse: Updated address data

    Raises:
        HTTPException: If address not found or doesn't belong to user
    """
    db_session = await db_session_gen.__anext__()
    
    # Get address and verify ownership
    result = await db_session.execute(
        select(Address)
        .where(Address.id == address_id)
        .where(Address.client_id == user.id)
    )
    db_address = result.scalar_one_or_none()
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    # If setting as default, update other addresses
    if address_update.is_default:
        await db_session.execute(
            select(Address)
            .where(Address.client_id == user.id)
            .where(Address.id != address_id)
            .update({"is_default": False})
        )
    
    # Update address fields
    for field, value in address_update.model_dump().items():
        setattr(db_address, field, value)
    
    await db_session.commit()
    await db_session.refresh(db_address)
    return db_address

@router.delete("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    db_session_gen: DBSessionDep,
    address_id: int,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Delete an address.

    Args:
        db_session_gen: Database session dependency
        address_id: ID of the address to delete
        user: Authenticated user from dependency

    Raises:
        HTTPException: If address not found or doesn't belong to user
    """
    db_session = await db_session_gen.__anext__()
    
    result = await db_session.execute(
        select(Address)
        .where(Address.id == address_id)
        .where(Address.client_id == user.id)
    )
    db_address = result.scalar_one_or_none()
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    await db_session.delete(db_address)
    await db_session.commit()
