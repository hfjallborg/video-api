from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'public_id', 'status', 'user', 'created',]
    list_filter = ['created',]
