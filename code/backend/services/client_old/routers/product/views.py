# own imports
from orm import Product, Review, Client, ProductImage
from .schema import (
    ProductCreate, ProductResponse, ProductListResponse, ProductUpdate,
    ProductReviewCreate, ProductReviewResponse, ProductImageCreate, ProductImageResponse,
    ProductFilter
)
from dependencies import validate_is_authenticated, validate_is_admin, DBSessionDep

# external imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from typing import List

# Router configuration
router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"]
)

@router.get("/", response_model=List[ProductListResponse])
async def list_products(
    db_session_gen: DBSessionDep,
    filters: ProductFilter = Depends(),
    skip: int = 0,
    limit: int = 20
):
    """
    List products with optional filters.
    
    Args:
        db_session_gen: Database session dependency
        filters: Product filters (type, price range, etc.)
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of products matching the filters
    """
    db_session = await db_session_gen.__anext__()
    query = select(Product)
    
    # Apply filters
    conditions = []
    if filters.product_type:
        conditions.append(Product.product_type == filters.product_type)
    if filters.for_baby is not None:
        conditions.append(Product.for_baby == filters.for_baby)
    if filters.min_price is not None:
        conditions.append(Product.price >= filters.min_price)
    if filters.max_price is not None:
        conditions.append(Product.price <= filters.max_price)
    if filters.size:
        conditions.append(Product.size == filters.size)
    if filters.color:
        conditions.append(Product.color == filters.color)
    if filters.line:
        conditions.append(Product.line == filters.line)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db_session.execute(query)
    return result.scalars().all()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    db_session_gen: DBSessionDep,
    product: ProductCreate,
    user: Client = Depends(validate_is_admin)
):
    """
    Create a new product.
    
    Args:
        db_session_gen: Database session dependency
        product: Product data
        user: Authenticated user (must be admin)
        
    Returns:
        Created product data
        
    Raises:
        HTTPException: If user is not authorized
    """
    db_session = await db_session_gen.__anext__()
    
    db_product = Product(**product.model_dump())
    db_session.add(db_product)
    await db_session.commit()
    await db_session.refresh(db_product)
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db_session_gen: DBSessionDep
):
    """
    Get detailed information about a specific product.
    
    Args:
        product_id: ID of the product
        db_session_gen: Database session dependency
        
    Returns:
        Product details
        
    Raises:
        HTTPException: If product not found
    """
    db_session = await db_session_gen.__anext__()
    result = await db_session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_admin)
):
    """
    Update a product.
    
    Args:
        product_id: ID of the product to update
        product_update: Updated product data
        db_session_gen: Database session dependency
        user: Authenticated user (must be admin)
        
    Returns:
        Updated product data
        
    Raises:
        HTTPException: If product not found or user not authorized
    """
    db_session = await db_session_gen.__anext__()
    
    result = await db_session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update product fields
    for field, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    
    await db_session.commit()
    await db_session.refresh(product)
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_admin)
):
    """
    Delete a product.
    
    Args:
        product_id: ID of the product to delete
        db_session_gen: Database session dependency
        user: Authenticated user (must be admin)
        
    Raises:
        HTTPException: If product not found or user not authorized
    """
    db_session = await db_session_gen.__anext__()
    
    result = await db_session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    await db_session.delete(product)
    await db_session.commit()

@router.post("/{product_id}/images", response_model=ProductImageResponse, status_code=status.HTTP_201_CREATED)
async def add_product_image(
    product_id: int,
    image: ProductImageCreate,
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_admin)
):
    """
    Add an image to a product.
    
    Args:
        product_id: ID of the product
        image: Image data
        db_session_gen: Database session dependency
        user: Authenticated user (must be admin)
        
    Returns:
        Created image data
        
    Raises:
        HTTPException: If product not found or user not authorized
    """
    db_session = await db_session_gen.__anext__()

    # Verify product exists
    result = await db_session.execute(
        select(Product).where(Product.id == product_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db_image = ProductImage(**image.model_dump())
    db_session.add(db_image)
    await db_session.commit()
    await db_session.refresh(db_image)
    return db_image

@router.get("/{product_id}/reviews", response_model=List[ProductReviewResponse])
async def get_product_reviews(
    product_id: int,
    db_session_gen: DBSessionDep,
    skip: int = 0,
    limit: int = 20
):
    """
    Get reviews for a specific product.
    
    Args:
        product_id: ID of the product
        db_session_gen: Database session dependency
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        
    Returns:
        List of product reviews
        
    Raises:
        HTTPException: If product not found
    """
    db_session = await db_session_gen.__anext__()
    
    # Verify product exists
    result = await db_session.execute(
        select(Product).where(Product.id == product_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Get reviews
    result = await db_session.execute(
        select(Review)
        .where(Review.product_id == product_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/{product_id}/reviews", response_model=ProductReviewResponse)
async def create_product_review(
    product_id: int,
    review: ProductReviewCreate,
    db_session_gen: DBSessionDep,
    user: Client = Depends(validate_is_authenticated)
):
    """
    Add a review for a specific product.
    
    Args:
        product_id: ID of the product
        review: Review data
        db_session_gen: Database session dependency
        user: Authenticated user
        
    Returns:
        Created review data
        
    Raises:
        HTTPException: If product not found
    """
    db_session = await db_session_gen.__anext__()
    
    # Verify product exists
    result = await db_session.execute(
        select(Product).where(Product.id == product_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if user has already reviewed this product
    result = await db_session.execute(
        select(Review)
        .where(Review.product_id == product_id)
        .where(Review.client_id == user.id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )
    
    # Create review
    db_review = Review(
        product_id=product_id,
        client_id=user.id,
        rating=review.rating,
        comment=review.comment
    )
    db_session.add(db_review)
    await db_session.commit()
    await db_session.refresh(db_review)
    return db_review
