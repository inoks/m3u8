from app.api.views import PlaylistViewSet, ChannelViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'playlists', PlaylistViewSet)

playlist_router = routers.NestedSimpleRouter(router, r'playlists', lookup='playlist')
playlist_router.register(r'channels', ChannelViewSet, base_name='playlist-channels')
