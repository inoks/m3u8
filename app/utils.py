import json
import logging
import random
import re
import string

import requests

logger = logging.getLogger(__name__)


class M3U8ChannelProxy(object):
    duration = None
    title = None
    extra_data = {}
    is_valid = True

    def __init__(self, extinf_string):
        try:
            self.duration = re.findall(r'EXTINF:(-?\d+)', extinf_string)[0]
            self.title = extinf_string.split(',')[-1]
        except IndexError as e:
            logging.warning('Unable to parse EXTINF string: {}. Error: {} '.format(extinf_string, e))
            self.is_valid = False
            return

        # Collect extra attrs
        extra_attrs = [
            'tvg-ID',
            'tvg-name',
            'tvg-logo',
            'group-title'
        ]
        for attr in extra_attrs:
            attr_values = re.findall(r'^.*(?i){attr}="([^"]*)".*'.format(attr=attr), extinf_string)
            if attr_values:
                self.extra_data[attr] = attr_values[0]


def generate_random_key(length=4):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def load_remote_m3u8(link, playlist, remove_existed=False):
    from app.models import Channel

    r = requests.get(link)
    if not r.ok:
        return

    if remove_existed:
        playlist.channels.all().delete()

    channel = None
    group = None
    for line in r.iter_lines(decode_unicode=True):
        if isinstance(line, bytes):
            line = line.decode("utf-8")

        if line == '#EXTM3U':
            continue

        if line.startswith('#EXTINF:'):
            channel = M3U8ChannelProxy(line)
            if not channel.is_valid:
                logger.warning('Unable to load EXTINF, format is not recognized: {}'.format(line))

            continue

        if line.startswith('#EXTGRP:'):
            group = line[8:]
            continue

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            continue

        if line and channel and channel.is_valid:
            path = line

            Channel.objects.create(
                playlist=playlist,
                title=channel.title,
                duration=channel.duration,
                group=group,
                extra_data=json.dumps(channel.extra_data) if channel.extra_data else None,
                path=path
            )
            channel = None

    return True


def load_m3u8_from_file(fo, playlist, remove_existed=False):
    from app.models import Channel

    # Rewind file to start again
    fo.file.seek(0)

    if remove_existed:
        playlist.channels.all().delete()

    channel = None
    group = None

    for line in fo.read().splitlines():
        line = line.decode("utf-8")

        if line == '#EXTM3U':
            continue

        if line.startswith('#EXTINF:'):
            channel = M3U8ChannelProxy(line)
            if not channel.is_valid:
                logger.error('Unable to load EXTINF, format is not recognized: {}'.format(line))

            continue

        if line.startswith('#EXTGRP:'):
            group = line[8:]
            continue

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            continue

        if line and channel and channel.is_valid:
            path = line

            Channel.objects.create(
                playlist=playlist,
                title=channel.title,
                duration=channel.duration,
                group=group,
                extra_data=json.dumps(channel.extra_data) if channel.extra_data else None,
                path=path
            )
            channel = None
