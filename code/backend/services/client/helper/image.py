from PIL import Image as PILImage
from io import BytesIO


class ImageHelper:
    @staticmethod
    def resize_image(image: PILImage.Image, dimensions: tuple[int, int]) -> BytesIO:
        """
        Resize an image to the specified dimensions while maintaining aspect ratio.
        
        Args:
            image (PILImage.Image): The image to resize
            dimensions (tuple[int, int]): Target dimensions (width, height)
            
        Returns:
            BytesIO: A BytesIO object containing the resized image
            
        Raises:
            ValueError: If dimensions are invalid (negative or zero)
        """
        # Validate dimensions
        width, height = dimensions
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive integers")
            
        # Resize image
        resized = image.copy()
        resized.thumbnail(dimensions)
        
        # Save to BytesIO
        buffer = BytesIO()
        resized.save(buffer, format=image.format or 'JPEG')
        buffer.seek(0)
        return buffer
