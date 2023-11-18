from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Video


class VideoTesting(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.client = APIClient()

        # First user
        cls.user1 = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.token1 = Token.objects.create(user=cls.user1)

        # Second user
        cls.user2 = User.objects.create_user(
            username="JohnDoe",
            password="secretpassword1234",
        )
        cls.token2 = Token.objects.create(user=cls.user2)

        # Video objects
        cls.video1 = Video(
            user=cls.user1,
            title="Testing video",
            description="This is a good description",
            status=Video.Status.PUBLIC,
        )
        cls.video1.save()
        cls.video1_pri = Video(
            user=cls.user1,
            title="Testing video 2",
            description="This is a good description",
            status=Video.Status.PRIVATE,
        )
        cls.video1_pri.save()
        cls.video2 = Video(
            user=cls.user2,
            title="Private video",
            description="This video should be private",
            status=Video.Status.PRIVATE,
        )
        cls.video2.save()

    def test_video_permissions_no_auth(self):
        # Video list view
        response = self.client.get(reverse('videos:video_list'))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(reverse('videos:video_list'),
                                    {'title': 'New video',
                                     'description': 'I want to upload this video',
                                     },)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('videos:video_detail', kwargs={'public_id': self.video1.public_id}))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('videos:video_source', kwargs={'public_id': self.video1.public_id}))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_video_permissions_with_token(self):
        # Access video list
        response = self.client.get(reverse('videos:video_list'), HTTP_AUTHORIZATION=f'Token {self.token1}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # TODO: Post video
        # with open(settings.BASE_DIR / 'videos/test.mp4', 'rb') as f:
        #     response = self.client.post(reverse('videos:video_list'),
        #                                 {'title': 'New video',
        #                                  'description': 'I want to upload this video',
        #                                  'file': f},
        #                                 format='multipart',
        #                                 HTTP_AUTHORIZATION=f'Token {self.token1}'
        #                                 )
        # self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Access public video detail
        response = self.client.get(reverse('videos:video_detail', kwargs={'public_id': self.video1.public_id}),
                                   HTTP_AUTHORIZATION=f'Token {self.token1}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # TODO: Access public video source
        # response = self.client.get(reverse('videos:video_source', kwargs={'public_id': self.video1.public_id}),
        #                            HTTP_AUTHORIZATION=f'Token {self.token1}')
        # self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Access own private video
        response = self.client.get(reverse('videos:video_detail',
                                           kwargs={'public_id': self.video1_pri.public_id}),
                                   HTTP_AUTHORIZATION=f'Token {self.token1}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Access private video (of other user)
        response = self.client.get(reverse('videos:video_detail',
                                           kwargs={'public_id': self.video2.public_id}),
                                   HTTP_AUTHORIZATION=f'Token {self.token1}')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
