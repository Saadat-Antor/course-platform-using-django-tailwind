from django.db import models
from cloudinary.models import CloudinaryField
import helpers

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

# COURSE Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.DRAFT)
    # image = models.ImageField(upload_to=handle_upload,blank=True, null=True)
    image = CloudinaryField("image", null=True)
    access = models.CharField(max_length=20,
                              choices=AccessRequirement.choices,
                              default=AccessRequirement.EMAIL_REQUIRED)
                                

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED