from django.urls import include, path

from app.api.routers import router, playlist_router

app_name = 'app'  # Fix until DRF 3.8 will be released

urlpatterns = [
    path('', include(router.urls)),
    path('', include(playlist_router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]