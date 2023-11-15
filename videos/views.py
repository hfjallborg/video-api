from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Video
from .serializers import VideoDetailSerializer, VideoListSerializer, VideoUploadSerializer
from .permissions import IsOwnerOrReadOnly


class VideoListView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
    parser_classes = [MultiPartParser]

    # Authentication and authorization
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # The MultiPartParser lets us parse the uploaded file
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoDetailSerializer
    lookup_field = 'public_id'

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def video_source_view(request, public_id):
    """Video source URL"""
    video = get_object_or_404(Video, public_id=public_id)
    return FileResponse(video.file)
