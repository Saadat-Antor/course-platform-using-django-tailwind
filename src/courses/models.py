from django.db import models



class AccessRequirement(models.TextChoices):
    ANYONE = 'publish', 'Published'
    EMAIL_REQUIRED = 'email_required', 'Email Required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'publish', 'Published'
    DRAFT = 'draft', 'Draft'
    COMING_SOON = 'soon', 'Coming Soon'

# COURSE Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.DRAFT)
    image = models.ImageField()
    access = models.CharField(max_length=10,
                              choices=AccessRequirement.choices,
                              default=AccessRequirement.ANYONE)
                                

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED