import cloudinary
from django.conf import settings


def cloudinary_init():       
    cloudinary.config( 
        cloud_name = settings.CLOUDINARY_CLOUD_NAME, 
        api_key = settings.CLOUDINARY_PUBLIC_API_KEY, 
        api_secret = settings.CLOUDINARY_SECRET_API_KEY,
        secure=True
    )