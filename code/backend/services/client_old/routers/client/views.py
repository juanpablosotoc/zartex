# own imports
from orm import Client, Afiliado
from helper import Encryption
from .schema import (
    UserCreate, UserResponse, Token, 
    AfiliadoCreate, UserUpdate
)
from dependencies import validate_is_authenticated, DBSessionDep

# external imports
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

# Router configuration
router = APIRouter(
    prefix="/api/v1/client",
    tags=["client"]
)

# Routes
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    db_session_gen: DBSessionDep,
    user: UserCreate,
):
    """
    Register a new user.

    Args:
        db_session_gen: Database session dependency
        user: User registration data

    Returns:
        UserResponse: Created user data

    Raises:
        HTTPException: If email already exists
    """
    db_session = await db_session_gen.__anext__()
    result = await db_session.execute(select(Client).where(Client.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = Client(
        email=user.email,
        password_hash=Encryption.hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name
    )
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user

@router.post("/token_oauth2", response_model=Token)
async def login_for_access_token(
    db_session_gen: DBSessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticate user and generate access token from OAuth2 password request form

    Args:
        db_session_gen: Database session dependency
        form_data: OAuth2 password request form containing username (email) and password

    Returns:
        Token object containing access token and token type

    Raises:
        HTTPException: If credentials are invalid
    """
    db_session = await db_session_gen.__anext__()
    result = await db_session.execute(select(Client).where(Client.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not Encryption.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = Encryption.generate_token(
        data={"user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    user: Client = Depends(validate_is_authenticated),
):
    """
    Get current user's profile information.

    Args:
        user: Authenticated user from dependency

    Returns:
        UserResponse: Current user's data
    """
    return user

@router.put("/me", response_model=UserResponse)
async def update_user(
    db_session_gen: DBSessionDep,
    user_update: UserUpdate,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Update current user's profile information.

    Args:
        db_session_gen: Database session dependency
        user_update: Updated user data
        user: Authenticated user from dependency

    Returns:
        UserResponse: Updated user data

    Raises:
        HTTPException: If email is already taken
    """
    db_session = await db_session_gen.__anext__()
    
    # Check if email is being changed and if it's already taken
    if user_update.email != user.email:
        result = await db_session.execute(
            select(Client).where(Client.email == user_update.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user fields
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    
    await db_session.commit()
    await db_session.refresh(user)
    return user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Delete current user's account.

    Args:
        db_session_gen: Database session dependency
        user: Authenticated user from dependency
    """
    db_session = await db_session_gen.__anext__()
    await db_session.delete(user)
    await db_session.commit()

@router.post("/afiliado", response_model=UserResponse)
async def become_afiliado(
    db_session_gen: DBSessionDep,
    afiliado_data: AfiliadoCreate,
    user: Client = Depends(validate_is_authenticated),
):
    """
    Register current user as an affiliate.

    Args:
        db_session_gen: Database session dependency
        afiliado_data: Affiliate registration data
        user: Authenticated user from dependency

    Returns:
        UserResponse: Updated user data

    Raises:
        HTTPException: If user is already an affiliate
    """
    db_session = await db_session_gen.__anext__()
    
    if user.is_afiliado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an afiliado"
        )
    
    # Create afiliado record
    db_afiliado = Afiliado(
        client_id=user.id,
        cell_phone=afiliado_data.cell_phone
    )
    db_session.add(db_afiliado)
    
    # Update user status
    user.is_afiliado = True
    
    await db_session.commit()
    await db_session.refresh(user)
    return user
