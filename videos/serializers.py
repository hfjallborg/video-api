from rest_framework.serializers import ModelSerializer, Serializer, CharField

from .models import Video
from accounts.serializers import UserSerializer


class VideoListSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)

    class Meta:
        model = Video
        fields = ['user', 'title', 'public_id', 'created', 'status']


class VideoDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Video
        fields = ['public_id', 'user', 'title', 'description', 'created', 'source', 'file', 'status']

    def create(self, validated_data):
        video_obj = Video.objects.create(**validated_data)
        return video_obj
