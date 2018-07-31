from app.api.views import PlaylistViewSet, ChannelViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'playlists', PlaylistViewSet)
router.register(r'channels', ChannelViewSet)
