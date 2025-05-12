from datetime import datetime
from pydantic import BaseModel


class ImageBase(BaseModel):
    small_url: str
    medium_url: str
    large_url: str

class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    updated_at: datetime
