# own imports
from orm import Image, Client
from .schema import (
    ImageResponse
)
from dependencies import validate_is_admin, DBSessionDep
from myAws.s3 import S3
from config import Config
import os
import uuid
from PIL import Image as PILImage
from io import BytesIO
from helper import ImageHelper

# external imports
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form


# Router configuration
router = APIRouter(
    prefix="/api/v1/image",
    tags=["image"]
)

@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
    db_session_gen: DBSessionDep,
    file: UploadFile = File(...),
    user: Client = Depends(validate_is_admin)
):
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read and process the image
        contents = await file.read()
        image = PILImage.open(BytesIO(contents))
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        
        urls = {}
        bucket_name = os.getenv("AWS_BUCKET_NAME")
        if not bucket_name:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AWS bucket name not configured"
            )
        
        for size_name, dimensions in Config.IMAGE_SIZES.items():
            try:
                buffer = ImageHelper.resize_image(image, dimensions)
                # Upload to S3
                object_name = Config.gen_object_name(size_name, filename)
                S3.upload_fileobj(bucket_name, object_name, buffer)
                
                # Generate URL
                urls[f"{size_name}_url"] = S3.generate_public_url(bucket_name, object_name)
            except Exception as e:
                # If any size fails, clean up any uploaded files
                for uploaded_size in urls:
                    try:
                        uploaded_object = Config.gen_object_name(uploaded_size, filename)
                        S3.delete_object(bucket_name, uploaded_object)
                    except:
                        pass
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to process image size {size_name}: {str(e)}"
                )
        
        # Create database record
        db_session = await db_session_gen.__anext__()
        db_image = Image(
            small_url=urls['small_url'],
            medium_url=urls['medium_url'],
            large_url=urls['large_url']
        )
        db_session.add(db_image)
        await db_session.commit()
        await db_session.refresh(db_image)
        
        return db_image
        
    except PILImage.UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}"
        )

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
