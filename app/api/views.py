import logging

from rest_framework import viewsets, permissions
from rest_framework.mixins import CreateModelMixin

from app.api.serializers import PlaylistSerializer, ChannelSerializer, SubmittedPlaylistSerializer
from app.models import Playlist, Channel
from app.utils import load_m3u8_from_file, load_remote_m3u8

logger = logging.getLogger(__name__)


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


class SubmittedPlaylistViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SubmittedPlaylistSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        playlist = Playlist.objects.get(pk=self.kwargs['playlist_pk'])
        obj = serializer.save(
            playlist=playlist,
            user=self.request.user
        )
        if obj.url:
            success = load_remote_m3u8(obj.url, playlist, obj.remove_existed)
        else:
            success = load_m3u8_from_file(obj.file, playlist, obj.remove_existed)

        if not success:
            logger.warning('Unable to load playlist %s' % obj.pk)

    def get_queryset(self):
        qs = super(SubmittedPlaylistViewSet, self).get_queryset()
        qs = qs.filter(playlist__user=self.request.user).filter(playlist=self.kwargs['playlist_pk'])
        return qs
