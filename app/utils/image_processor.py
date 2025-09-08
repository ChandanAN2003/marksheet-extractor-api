from PIL import Image, ImageEnhance, ImageFilter

def resize_image(image: Image.Image) -> Image.Image:
    """
    Resizes the image to a maximum dimension to reduce memory usage.
    """
    max_dim = 2000
    if image.width > max_dim or image.height > max_dim:
        image.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    return image

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Applies image enhancements to improve OCR accuracy.
    """
    # Convert to grayscale to remove color noise
    img = image.convert('L')
    
    # Increase contrast to make text stand out
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Apply a sharpening filter
    img = img.filter(ImageFilter.SHARPEN)
    
    return img