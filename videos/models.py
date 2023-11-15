from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

from shortuuidfield import ShortUUIDField


class Video(models.Model):
    class Status(models.TextChoices):
        PUBLIC = 'PUB', 'Public'
        PRIVATE = 'PRI', 'Private'
        DELETED = 'DEL', 'Deleted'

    # A non-numeric id will be used for public access
    public_id = ShortUUIDField(editable=False, unique=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.PRIVATE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='videos_uploaded')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='%Y/%m/%d/%H/%M/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def source(self):
        return reverse_lazy('videos:video_source', kwargs={"public_id": self.public_id})
