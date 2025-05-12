# own imports
from orm import Image, Client
from .schema import (
    ImageCreate, ImageResponse
)
from dependencies import validate_is_admin, DBSessionDep

# external imports
from fastapi import APIRouter, Depends, HTTPException, status

# Router configuration
router = APIRouter(
    prefix="/api/v1/image",
    tags=["image"]
)

@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
    db_session_gen: DBSessionDep,
    image: ImageCreate,
    user: Client = Depends(validate_is_admin)
):
    db_session = await db_session_gen.__anext__()
    db_image = Image(**image.model_dump())
    db_session.add(db_image)
    await db_session.commit()
    await db_session.refresh(db_image)
    return db_image

@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(
    image_id: int,
    db_session_gen: DBSessionDep
):
    db_session = await db_session_gen.__anext__()
    db_image = db_session.get(Image, image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return db_image

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: int,
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_admin)
):
    db_session = await db_session_gen.__anext__()
    db_image = db_session.get(Image, image_id)
    if not db_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    await db_session.delete(db_image)
    await db_session.commit()
