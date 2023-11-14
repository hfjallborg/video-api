from django.urls import path

from . import views

app_name = 'videos'

urlpatterns = [
    path('api/v/', views.VideoListView.as_view(), name='video_list'),
    path('api/v/<str:public_id>/', views.VideoRetrieveView.as_view(), name='video_detail'),
    path('api/v/<str:public_id>/source/', views.video_source_view, name='video_source'),
  #  path('api/v/upload/', views.VideoUploadView.as_view(), name='video_upload')
]
