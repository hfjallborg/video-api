from django.urls import path

from . import views

app_name = 'videos'

urlpatterns = [
    path('api/videos/', views.VideoListView.as_view(), name='video_list'),
    path('api/videos/<str:public_id>/', views.VideoRetrieveView.as_view(), name='video_detail'),
    path('api/videos/<str:public_id>/source/', views.video_source_view, name='video_source'),
]
