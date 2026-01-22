from django.db import models
from cloudinary.models import CloudinaryField
import helpers
from django.utils.text import slugify

helpers.cloudinary_init()


class AccessRequirement(models.TextChoices):
    ANYONE = 'anyone', 'Anyone'
    EMAIL_REQUIRED = 'email_required', 'Email Required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'publish', 'Published'
    DRAFT = 'draft', 'Draft'
    COMING_SOON = 'soon', 'Coming Soon'


def handle_upload(instance, filename):
    return f"{filename}"

def get_public_id_prefix(instance, *args, **kwargs):
    if instance.title:
        slug = slugify(instance.title)
        return f"courses/{slug}"
    elif instance.id:
        return f"courses/{instance.id}"
    return "courses"

def get_display_name(instance, *args, **kwargs):
    if instance.title:
        return instance.title
    return "Course Upload"


# COURSE Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.DRAFT)
    # image = models.ImageField(upload_to=handle_upload,blank=True, null=True)
    image = CloudinaryField("image", 
                            null=True, 
                            public_id_prefix=get_public_id_prefix, 
                            tags=["course", "thumbnail"]
                            )
    access = models.CharField(max_length=20,
                              choices=AccessRequirement.choices,
                              default=AccessRequirement.EMAIL_REQUIRED
                              )
    created = models.DateTimeField(auto_now_add=True)
                                

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        image_options = {
            "width": 200
        }
        url =self.image.build_url(**image_options)
        return url
    

    def get_image_thumbnail(self, as_html=False, width=500):
        if not self.image:
            return ""
        image_options = {
            "width": width
        }
        if as_html:
            return self.image.image(**image_options)
        url =self.image.build_url(**image_options)
        return url
    
# LESSON Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="Can students view this lesson without enrolling?")
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.PUBLISHED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-updated']