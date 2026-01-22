from django.db import models
from cloudinary.models import CloudinaryField
import helpers
from django.utils.text import slugify
import uuid

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

def generate_public_id(instance, *args, **kwargs):
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not instance.title:
        return unique_id
    slug = slugify(instance.title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"


def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    model_name_slug = slugify(instance.__class__.__name__)
    if not instance.public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{instance.public_id}"

def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    
    model_name = instance.__class__.__name__
    return f"{model_name} Upload"


# COURSE Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.DRAFT)
    # image = models.ImageField(upload_to=handle_upload,blank=True, null=True)
    image = CloudinaryField("image", 
                            null=True, 
                            public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name,
                            tags=["course", "thumbnail"]
                            )
    access = models.CharField(max_length=20,
                              choices=AccessRequirement.choices,
                              default=AccessRequirement.EMAIL_REQUIRED
                              )
    created = models.DateTimeField(auto_now_add=True)

    def get_display_name(self):
        return f"{self.title} - Course"

    def get_absolute_path(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.public_id}"                      

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    
# LESSON Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image",
                                public_id_prefix=get_public_id_prefix,
                                display_name=get_display_name,
                                tags=["thumbnail", "lesson"],
                                blank=True, 
                                null=True
                                )
    video = CloudinaryField("video", 
                            public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name,
                            tags=["video", "lesson"],
                            type='private',
                            blank=True, 
                            null=True, 
                            resource_type="video"
                            )
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="Can students view this lesson without enrolling?")
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.PUBLISHED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-updated']

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"


    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/{self.public_id}" 