from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status


class UserViewsTesting(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.normal_user = User.objects.create(
            username='testuser',
            password='testpass123',
        )
        cls.normal_user_token = Token.objects.create(user=cls.normal_user)
        cls.staff_user = User.objects.create_superuser(
            username='adminuser',
            password='secretpass123',
        )
        cls.staff_user_token = Token.objects.create(user=cls.staff_user)

    def test_view_permissions_no_auth(self):
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_permissions_no_staff(self):
        response = self.client.get(reverse('accounts:user_list'),
                                   HTTP_AUTHORIZATION=f'Token {self.normal_user_token}')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_permissions_staff(self):
        response = self.client.get(reverse('accounts:user_list'),
                                   HTTP_AUTHORIZATION=f'Token {self.staff_user_token}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        response = self.client.post(reverse('accounts:user_list'),
                                    {'username': 'new-user',
                                     'password': 'newpassword123'},
                                    HTTP_AUTHORIZATION=f'Token {self.staff_user_token}')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # Check if token has been generated
        # .filter is used instead of get to avoid having to use a try/except to catch DoesNotExist
        self.assertTrue(Token.objects.filter(user__username='new-user').exists())
