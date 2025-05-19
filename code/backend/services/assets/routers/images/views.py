# own imports
from myOrm.models import Image, Client
from .schema import ImageResponse
from myDependencies import validate_is_admin
from myAws.s3 import S3
from config import Config, logger
import os
import uuid
from PIL import Image as PILImage
from io import BytesIO
from helper import ImageHelper

# external imports
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from myOrm import get_db_session

# Router configuration
router = APIRouter(
    prefix="/api/v1/assets/images",
    tags=["images"]
)

@router.post(
    "/",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_image(
    db_session: AsyncSession = Depends(get_db_session),
    file: UploadFile = File(...),
    user: Client = Depends(validate_is_admin)
):
    start_time = datetime.now()
    logger.info(f"Starting image upload process for file: {file.filename}")

    # Validate file size
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {Config.MAX_FILE_SIZE/1024/1024}MB"
            )
    await file.seek(0)

    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in Config.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension not allowed. Allowed extensions: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        )

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
        
        # Validate image dimensions
        if max(image.size) > Config.MAX_IMAGE_DIMENSION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image dimensions exceed maximum allowed size of {Config.MAX_IMAGE_DIMENSION}x{Config.MAX_IMAGE_DIMENSION} pixels"
            )

        # Generate unique filename
        filename = f"{uuid.uuid4()}{file_ext}"
        urls = {}
        bucket_name = os.getenv("AWS_BUCKET_NAME")
        if not bucket_name:
            logger.error("AWS bucket name not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AWS bucket name not configured"
            )
        
        for size_name, dimensions in Config.IMAGE_SIZES.items():
            buffer = ImageHelper.resize_image(image, dimensions)
            object_name = Config.gen_object_name(size_name, filename)
            S3.upload_fileobj(bucket_name, object_name, buffer)
            urls[f"{size_name}_url"] = S3.generate_public_url(bucket_name, object_name)
            logger.info(f"Successfully processed and uploaded {size_name} size for {filename}")
        
        # Create database record
        db_image = Image(
            small_url=urls['small_url'],
            medium_url=urls['medium_url'],
            large_url=urls['large_url']
        )
        db_session.add(db_image)
        await db_session.commit()
        await db_session.refresh(db_image)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Successfully processed image {filename} in {processing_time:.2f} seconds")
        return db_image
    except PILImage.UnidentifiedImageError:
        logger.error(f"Invalid image file: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file"
        )
    except HTTPException:
        # Let FastAPI handle HTTPExceptions (e.g. our 400s)
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}"
        )

@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(
    image_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    logger.info(f"Fetching image with ID: {image_id}")
    db_image = await db_session.get(Image, image_id)
    if not db_image:
        logger.warning(f"Image not found with ID: {image_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Image not found"
        )
    logger.info(f"Successfully retrieved image with ID: {image_id}")
    return db_image

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: int,
    db_session: AsyncSession = Depends(get_db_session),
    user: Client = Depends(validate_is_admin)
):
    logger.info(f"Attempting to delete image with ID: {image_id}")
    db_image = await db_session.get(Image, image_id)
    if not db_image:
        logger.warning(f"Image not found for deletion with ID: {image_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Image not found"
        )

    # Delete from S3
    filename = next(
        (url.split('/')[-1] for url in [db_image.small_url, db_image.medium_url, db_image.large_url] if url),
        None
    )
    if filename:
        bucket_name = os.getenv("AWS_BUCKET_NAME")
        if bucket_name:
            for size_name in Config.IMAGE_SIZES.keys():
                object_name = Config.gen_object_name(size_name, filename)
                try:
                    S3.delete_object(bucket_name, object_name)
                    logger.info(f"Deleted {size_name} size from S3 for image {image_id}")
                except Exception:
                    logger.exception(f"Failed to delete {size_name} size from S3 for image {image_id}")

    # Delete from database
    await db_session.delete(db_image)
    await db_session.commit()
    logger.info(f"Successfully deleted image with ID: {image_id}")
