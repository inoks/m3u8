import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.api.permissions import IsOwnerOnly
from app.api.serializers import PlaylistSerializer, ChannelSerializer
from app.models import Playlist, Channel

logger = logging.getLogger(__name__)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = (IsOwnerOnly, )

    def get_queryset(self):
        qs = super(PlaylistViewSet, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(url_path='channels', methods=['get'], detail=True)
    def channels_list(self, *args, **kwargs):
        playlist = self.get_object()
        channels_qs = playlist.channel_set.all()
        serializer = ChannelSerializer(channels_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (IsOwnerOnly,)

    def get_queryset(self):
        qs = super(ChannelViewSet, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
