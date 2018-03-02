import logging
import random
import string

import m3u8

import requests
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


def generate_random_key(length=4):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def load_remote_m3u8(link, playlist, remove_existed=False):
    from app.models import Channel, Upload

    r = requests.get(link)
    if not r.ok:
        return

    upload = Upload(
        user=playlist.user,
        info=link
    )
    upload.file.save('requests.m3u8', ContentFile(r.content))
    upload.save()

    if remove_existed:
        playlist.channels.all().delete()

    channels = m3u8.load(link)

    if channels.segments:
        for segment in channels.segments:
            Channel.objects.create(
                playlist=playlist,
                title=segment.title if segment.title else None,
                duration=segment.duration if segment.duration else None,
                group=segment.group if hasattr(segment, 'group') else None,
                path=segment.uri
            )


def load_m3u8_from_file(fo, playlist, remove_existed=False):
    from app.models import Channel, Upload

    Upload.objects.create(
        user=playlist.user,
        info=fo.name,
        file=fo
    )

    # Rewind file to start again
    fo.file.seek(0)
    content = fo.read().decode('utf-8')

    if remove_existed:
        playlist.channels.all().delete()

    channels = m3u8.loads(content)

    if channels.segments:
        for segment in channels.segments:
            Channel.objects.create(
                playlist=playlist,
                title=segment.title if segment.title else None,
                duration=segment.duration if segment.duration else None,
                group=segment.group if hasattr(segment, 'group') else None,
                path=segment.uri
            )
