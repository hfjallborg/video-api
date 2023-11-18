from django.contrib.auth import get_user_model

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


class UserListView(ListCreateAPIView):
    """This view lists users and manages creation of new users.

    This view is restricted to staff users only.
    """
    permission_classes = [IsAdminUser,]

    user_model = get_user_model()
    queryset = user_model.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_model = get_user_model()
            user = user_model.objects.create_user(**serializer.validated_data)
            # Generate a token for the new user
            Token.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
