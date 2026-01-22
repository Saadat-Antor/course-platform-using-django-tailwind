from django.contrib import admin
from .models import Course, Lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage

# Register your models here.

class LessonInline(admin.StackedInline):
    model = Lesson
    extra=0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

    list_display = ["title", "status", "access"]
    list_filter = ["status", "access"]

    fields = ["title", "description", "status", "image", "access", "display_image"]

    readonly_fields = ["display_image"]
    
    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin_url
        return format_html(f"<img src='{url}'/>")
    
    display_image.short_description = "Current Image"
