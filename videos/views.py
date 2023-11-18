from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Video
from .serializers import VideoDetailSerializer, VideoListSerializer
from .permissions import VideoStatusPermission


class VideoListView(generics.ListCreateAPIView):
    """Response contains a list of videos depending on the users role.

    Normal users will get a list of public videos and their own videos (excluding deleted videos). Staff users will get
    the full list of videos, regardless of status.
    """
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
    parser_classes = [MultiPartParser]

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Video.objects.all()
        else:
            public_videos = Video.objects.filter(status=Video.Status.PUBLIC)
            user_videos = Video.objects.filter(user=user).exclude(status=Video.Status.DELETED)
            return public_videos | user_videos

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # The MultiPartParser lets us parse the uploaded file
        serializer = VideoDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """View or change data of the video with the provided public_id."""
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    lookup_field = 'public_id'

    permission_classes = [IsAuthenticated, VideoStatusPermission]

    def delete(self, request, *args, **kwargs):
        # Instead of permanently deleting the video, the 'DELETE' request will set 'DEL'-status
        video = self.get_object()
        video.status = Video.Status.DELETED
        video.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, VideoStatusPermission])
def video_source_view(request, public_id):
    """Video source URL"""
    video = get_object_or_404(Video, public_id=public_id)
    return FileResponse(video.file)
