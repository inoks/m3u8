import logging
import random
import re
import string

import requests
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


class M3U8Channel(object):
    duration = None
    title = None
    is_valid = True

    def __init__(self, extinf_string):
        try:
            self.duration = re.findall(r'EXTINF:(-?\d+)', extinf_string)[0]
            self.title = extinf_string.split(',')[-1]
        except IndexError as e:
            logging.warning('Unable to parse EXTINF string: {}. Error: {} '.format(extinf_string, e))
            self.is_valid = False


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

    duration = title = group = path = None
    for line in r.iter_lines(decode_unicode=True):
        if isinstance(line, bytes):
            line = line.decode("utf-8")

        if line == '#EXTM3U':
            continue

        if line.startswith('#EXTINF:'):
            channel = M3U8Channel(line)
            if channel.is_valid:
                duration = channel.duration
                title = channel.title
                continue

        if line.startswith('#EXTGRP:'):
            group = line[8:]
            continue

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            continue

        if line:
            path = line

            Channel.objects.create(
                playlist=playlist,
                title=title,
                duration=duration,
                group=group,
                path=path
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

    if remove_existed:
        playlist.channels.all().delete()

    duration = title = group = None

    for line in fo.read().splitlines():
        line = line.decode("utf-8")

        if line == '#EXTM3U':
            continue

        if line.startswith('#EXTINF:'):
            channel = M3U8Channel(line)
            if channel.is_valid:
                duration = channel.duration
                title = channel.title
                continue

        if line.startswith('#EXTGRP:'):
            group = line[8:]
            continue

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            continue

        if line:
            path = line

            Channel.objects.create(
                playlist=playlist,
                title=title,
                duration=duration,
                group=group,
                path=path
            )
