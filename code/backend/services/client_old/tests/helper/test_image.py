import pytest
from PIL import Image
from io import BytesIO
from helper.image import ImageHelper
from config import Config

@pytest.fixture
def sample_image():
    # Create a 1000x1000 test image
    img = Image.new('RGB', (1000, 1000), color='red')
    return img


def test_resize_image_dimensions(sample_image):
    # Test resizing to smaller dimensions
    dimensions = (300, 300)
    result = ImageHelper.resize_image(sample_image, dimensions)
    
    # Convert BytesIO back to PIL Image to check dimensions
    result_image = Image.open(result)
    assert result_image.width <= dimensions[0]
    assert result_image.height <= dimensions[1]
    
    # Check aspect ratio is maintained
    original_ratio = sample_image.width / sample_image.height
    result_ratio = result_image.width / result_image.height
    assert abs(original_ratio - result_ratio) < 0.01  # Allow small floating point differences


def test_resize_image_format(sample_image):
    # Test that the output format matches the input format
    dimensions = (300, 300)
    result = ImageHelper.resize_image(sample_image, dimensions)
    
    # Convert BytesIO back to PIL Image to check format
    result_image = Image.open(result)
    assert result_image.format == 'JPEG'  # Default format when no format is specified


def test_resize_image_larger_dimensions(sample_image):
    # Test resizing to larger dimensions (should maintain original size)
    dimensions = (2000, 2000)
    result = ImageHelper.resize_image(sample_image, dimensions)
    
    # Convert BytesIO back to PIL Image to check dimensions
    result_image = Image.open(result)
    assert result_image.width == sample_image.width
    assert result_image.height == sample_image.height


def test_resize_image_invalid_dimensions(sample_image):
    # Test with invalid dimensions
    invalid_dimensions = [
        (-1, -1),
        (-1, 100),
        (100, -1),
        (0, 0),
        (0, 100),
        (100, 0)
    ]
    
    for dimensions in invalid_dimensions:
        with pytest.raises(ValueError, match="Dimensions must be positive integers"):
            ImageHelper.resize_image(sample_image, dimensions)


def test_resize_image_aspect_ratio(sample_image):
    # Test resizing with different aspect ratios
    test_dimensions = [
        (300, 200),  # Wider than original
        (200, 300),  # Taller than original
        (300, 300),  # Square
    ]
    
    for dimensions in test_dimensions:
        result = ImageHelper.resize_image(sample_image, dimensions)
        result_image = Image.open(result)
        
        # Check that the image fits within the target dimensions
        assert result_image.width <= dimensions[0]
        assert result_image.height <= dimensions[1]
        
        # Check that aspect ratio is maintained
        original_ratio = sample_image.width / sample_image.height
        result_ratio = result_image.width / result_image.height
        assert abs(original_ratio - result_ratio) < 0.01 