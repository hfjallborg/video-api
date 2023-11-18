from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('api/users/', views.UserListView.as_view(), name='user_list'),
]
