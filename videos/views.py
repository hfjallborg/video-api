from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Video
from .serializers import VideoDetailSerializer, VideoListSerializer


class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer


class VideoRetrieveView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    lookup_field = 'public_id'


@api_view()
def video_source_view(request, public_id):
    """Video source URL"""
    video = get_object_or_404(Video, public_id=public_id)
    return FileResponse(video.file)
