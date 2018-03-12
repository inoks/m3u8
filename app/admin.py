from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from app.models import Channel, Playlist, Upload


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'group', 'playlist', 'created_at']
    search_fields = ['title', 'group', 'path']
    list_filter = ['created_at', 'playlist', ]
    ordering = ['-created_at']


class PlaylistAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'public_key', 'public_link', ]
    list_display = ['user', 'count', 'created_at']


class UploadAdmin(admin.ModelAdmin):
    list_display = ['info', 'user', 'created_at']


class EnhancedUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('date_joined', )
    ordering = ('-date_joined', )


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Upload, UploadAdmin)

admin.site.unregister(User)
admin.site.register(User, EnhancedUserAdmin)
