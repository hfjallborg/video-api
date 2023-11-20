from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'accounts'

urlpatterns = [
    path('api/users/', views.UserListView.as_view(), name='user_list'),

    # Authentication views
    path('api/auth/get_token/', obtain_auth_token, name='get_auth_token'),
]
