from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class ProductImageBase(BaseModel):
    image_id: int
    product_id: int

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    image_id: int
    small_url: str
    medium_url: str
    large_url: str

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    product_type: str = Field(..., min_length=1, max_length=50)
    for_baby: bool
    size: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    line: Optional[str] = Field(None, max_length=50)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    product_type: Optional[str] = Field(None, min_length=1, max_length=50)
    for_baby: Optional[bool] = None
    size: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    line: Optional[str] = Field(None, max_length=50)

class ProductResponse(ProductBase):
    id: int
    current_quantity: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True

class ProductListResponse(ProductBase):
    id: int
    current_quantity: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True

class ProductReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ProductReviewCreate(ProductReviewBase):
    pass

class ProductReviewResponse(ProductReviewBase):
    id: int
    product_id: int
    client_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductFilter(BaseModel):
    product_type: Optional[str] = None
    for_baby: Optional[bool] = None
    min_price: Optional[float] = Field(None, gt=0)
    max_price: Optional[float] = Field(None, gt=0)
    size: Optional[str] = None
    color: Optional[str] = None
    line: Optional[str] = None

    @validator('max_price')
    def max_price_must_be_greater_than_min_price(cls, v, values):
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v <= values['min_price']:
                raise ValueError('max_price must be greater than min_price')
        return v
