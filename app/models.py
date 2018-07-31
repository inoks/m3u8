import json
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    public_key = models.CharField(max_length=8, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if not self.public_key:
            self.public_key = get_random_string(length=6, allowed_chars=string.ascii_letters)

        super(Playlist, self).save(**kwargs)

    @cached_property
    def public_link(self):
        if self.public_key:
            return settings.BASE_PATH + reverse('playlist-public', kwargs={'public_key': self.public_key})

    def __str__(self):
        return 'Playlist {}, user: {}'.format(self.pk, self.user)

    @cached_property
    def count(self):
        return self.channel_set.all().count()


class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    duration = models.CharField(default='0', max_length=255)
    group = models.CharField(max_length=255, null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)
    path = models.TextField(_('Path to content'))
    hidden = models.BooleanField(_('Hide from public playlist'), default=False)
    playlists = models.ManyToManyField(Playlist, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.is_secure:
            return settings.BASE_PATH + reverse('channel', kwargs={'pk': self.pk})
        else:
            return settings.UNSECURE_BASE_PATH + reverse('channel', kwargs={'pk': self.pk})

    @cached_property
    def is_secure(self):
        return self.path and self.path.startswith('https://')

    @cached_property
    def extra_data_dict(self):
        if self.extra_data:
            return json.loads(self.extra_data)
        else:
            return {}

    def extinf(self):
        if self.extra_data:
            return '{duration}, ' \
                   'tvg-ID="{tvg_id}" ' \
                   'tvg-name="{tvg_name}" ' \
                   'tvg-logo="{tvg_logo}" ' \
                   'group-title="{group_title}",' \
                   '{title}' \
                .format(
                    duration=self.duration,
                    tvg_id=self.extra_data_dict.get('tvg-ID', ''),
                    tvg_name=self.extra_data_dict.get('tvg-name', ''),
                    tvg_logo=self.extra_data_dict.get('tvg-logo', ''),
                    group_title=self.extra_data_dict.get('group-title', ''),
                    title=self.title
                )
        else:
            return '{},{}'.format(self.duration, self.title)


class SubmittedPlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to='playlists', null=True, blank=True, validators=[FileExtensionValidator(['m3u8', 'm3u'])])
    url = models.URLField(null=True, blank=True)
    remove_existed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
