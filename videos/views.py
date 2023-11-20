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
        """Generates the list of videos for this view.

        Accepts URL parameters for filtering and sorting videos.
        """
        user = self.request.user

        filter_params = {}
        order_param = None

        if self.request.method == 'GET':

            # Filtering parameters
            if self.request.GET.get('user', None):
                filter_params['user__username'] = self.request.GET['user']
            if self.request.GET.get('status', None):
                status_query = self.request.GET['status']
                # This dict-comp translates the read-friendly url parameter (e.g. 'public') to the status code
                # (e.g. 'PUB'). There might be a better way to implement this.
                status_value = {choice[1].lower(): choice[0] for choice in Video.Status.choices}[status_query]
                filter_params['status'] = status_value

            # Sorting parameters
            if self.request.GET.get('sort_by', None):
                order_param = self.request.GET['sort_by']
            if self.request.GET.get('order_by', None):
                if self.request.GET['order_by'] == 'desc':
                    order_param = f'-{order_param}'

        queryset = Video.objects.filter(**filter_params)
        if order_param is not None:
            queryset = queryset.order_by(order_param)

        if user.is_staff:
            return queryset
        else:
            public_videos = queryset.filter(status=Video.Status.PUBLIC)
            user_videos = queryset.filter(user=user).exclude(status=Video.Status.DELETED)
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
