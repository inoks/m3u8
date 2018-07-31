from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from app.models import Channel, Playlist, SubmittedPlaylist


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'group', 'user', 'created_at']
    search_fields = ['title', 'group', 'path']
    list_filter = ['created_at', ]
    ordering = ['-created_at']
    raw_id_fields = ['user', 'playlists']


class PlaylistAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'public_key', 'public_link', ]
    list_display = ['user', 'count', 'created_at']
    raw_id_fields = ['user', ]


class SubmittedPlaylistAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'created_at']
    raw_id_fields = ['user', ]


class EnhancedUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('date_joined', 'last_login')
    list_filter = UserAdmin.list_filter + ('date_joined', 'last_login')
    ordering = ('-date_joined', )


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(SubmittedPlaylist, SubmittedPlaylistAdmin)

admin.site.unregister(User)
admin.site.register(User, EnhancedUserAdmin)
