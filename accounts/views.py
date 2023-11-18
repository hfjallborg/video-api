from django.contrib.auth import get_user_model

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import UserSerializer


class UserListView(ListCreateAPIView):
    """This view lists users and manages creation of new users.

    This view is restricted to staff users only.
    """
    permission_classes = [IsAdminUser,]

    user_model = get_user_model()
    queryset = user_model.objects.all()
    serializer_class = UserSerializer
