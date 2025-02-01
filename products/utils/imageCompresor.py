import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def optimize_image(image_file, max_width=1024, max_height=1024, quality=85):
    """
    Optimize an image by resizing and compressing it.
    """
    # Open the image file using Pillow
    image = Image.open(image_file)

    # Convert image to RGB if needed (e.g., if the image is in a different mode)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Resize the image while maintaining aspect ratio
    image.thumbnail((max_width, max_height), Image.LANCZOS)

    # Save the optimized image to a BytesIO buffer
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG', quality=quality)
    img_io.seek(0)

    # Create a new InMemoryUploadedFile (this simulates a file upload)
    optimized_image = InMemoryUploadedFile(
        img_io,
        field_name=None,
        name=image_file.name,
        content_type='image/jpeg',
        size=img_io.getbuffer().nbytes,
        charset=None
    )
    return optimized_image
