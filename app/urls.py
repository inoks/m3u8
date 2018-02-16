from django.urls import path
from django.views.generic import TemplateView
from app import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='app/index.html'), name='index'),
    path('add/', views.CreatePlaylist.as_view(), name='create-playlist'),
    path('channel/<int:pk>/', views.ChannelUpdate.as_view(), name='channel'),
    path('channel/new/', views.ChannelCreate.as_view(), name='new-channel'),
    path('channels', views.ChannelList.as_view(), name='channels'),
    path('public/<slug:public_key>.m3u8', views.public_playlist, name='playlist-public'),
]
