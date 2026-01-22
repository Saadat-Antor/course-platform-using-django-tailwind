from django.contrib import admin
from .models import Course
from django.utils.html import format_html
from cloudinary import CloudinaryImage

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "access"]
    list_filter = ["status", "access"]

    fields = ["title", "description", "status", "image", "access", "display_image"]

    readonly_fields = ["display_image"]
    
    def display_image(self, obj, *args, **kwargs):
        cloudinary_id = obj.image.public_id
        cloudinary_image_html = CloudinaryImage(cloudinary_id).image(width=500)
        return format_html(cloudinary_image_html)
    
    display_image.short_description = "Current Image"
