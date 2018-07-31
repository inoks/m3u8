from django.urls import path, include

from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.CreatePlaylist.as_view(), name='create-playlist'),
    path('channel/<int:pk>/', views.ChannelUpdate.as_view(), name='channel'),
    path('channel/new/', views.ChannelCreate.as_view(), name='new-channel'),
    path('channels', views.ChannelList.as_view(), name='channels'),
    path('react', views.ReactIndexView.as_view(), name='react'),
    path('public/<slug:public_key>.m3u8', views.PublicPlaylistView.as_view(), name='playlist-public'),

    path('api/', include('app.api.urls', namespace='api')),
]
