from rest_framework import viewsets, permissions

from app.api.serializers import PlaylistSerializer, ChannelSerializer
from app.models import Playlist, Channel


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = super(PlaylistViewSet, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = super(ChannelViewSet, self).get_queryset()
        qs = qs.filter(playlist__user=self.request.user).filter(playlist=self.kwargs['playlist_pk'])
        return qs

    def perform_create(self, serializer):
        playlist = Playlist.objects.get(pk=self.kwargs['playlist_pk'])
        serializer.save(playlist=playlist)
