from django.db import models
from django.conf import settings


class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='%Y/%m/%d/%H/%M/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
