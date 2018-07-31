import json
import logging
import re

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class M3U8ChannelFactory(object):
    group = None
    duration = None
    title = None
    path = None

    extra_data = {}

    def init_channel(self, extinf_string):
        logger.info('Init channel: %s', extinf_string)
        self.duration = None
        self.title = None
        self.group = None
        self.path = None
        self.extra_data = dict()

        try:
            duration = re.findall(r'EXTINF:(-?\d+)', extinf_string)[0]
            title = extinf_string.split(',')[-1]

            self.title = title
            self.duration = duration

        except IndexError as e:
            logging.warning('Unable to parse EXTINF string: {}. Error: {} '.format(extinf_string, e))
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

    def process_line(self, line):
        """ Add line to the channel """
        logger.info('Processing line: %s', line)

        if not line:
            return

        if isinstance(line, bytes):
            line = line.decode("utf-8", errors="ignore")

        if line == '#EXTM3U':
            return

        if line.startswith('#EXTINF:'):
            self.init_channel(line)
            return

        if line.startswith('#EXTGRP:'):
            self.group = line[8:]
            return

        if line.startswith('#'):
            logger.warning('Unsupported line skipped: {}'.format(line))
            return

        # Line without hash is the last in the channel definition and it is the path
        logger.info('Adding path: %s', line)
        self.path = line

    def get_extra_data(self):
        if self.extra_data:
            return json.dumps(self.extra_data)
        else:
            return None

    def is_complete(self):
        logger.info('Checking if channel complete')
        return all([self.path, self.title, self.group, self.duration])


def load_remote_m3u8(link, playlist, remove_existed=False):
    from app.models import Channel

    r = requests.get(link)
    if not r.ok:
        return False

    if remove_existed:
        Channel.objects.filter(playlists=playlist).delete()

    channel_factory = M3U8ChannelFactory()
    channel_count = 0
    for line in r.iter_lines(decode_unicode=True):
        channel_factory.process_line(line)
        if channel_factory.is_complete():
            channel_count += 1
            if channel_count > settings.MAX_CHANNELS:
                logger.warning('Too many channels, only %s was loaded', settings.MAX_CHANNELS)
                return False

            channel_obj = Channel.objects.create(
                user=playlist.user,
                title=channel_factory.title,
                duration=channel_factory.duration,
                group=channel_factory.group,
                extra_data=channel_factory.get_extra_data(),
                path=channel_factory.path
            )
            channel_obj.playlists.add(playlist)

    return True


def load_m3u8_from_file(fo, playlist, remove_existed=False):
    from app.models import Channel

    if remove_existed:
        Channel.objects.filter(playlists=playlist).delete()

    channel_factory = M3U8ChannelFactory()
    channel_count = 0
    for line in fo.read().splitlines():
        channel_factory.process_line(line)
        if channel_factory.is_complete():
            channel_count += 1
            if channel_count > settings.MAX_CHANNELS:
                logger.warning('Too many channels, only %s was loaded', settings.MAX_CHANNELS)
                return False

            channel_obj = Channel.objects.create(
                user=playlist.user,
                title=channel_factory.title,
                duration=channel_factory.duration,
                group=channel_factory.group,
                extra_data=channel_factory.get_extra_data(),
                path=channel_factory.path
            )
            channel_obj.playlists.add(playlist)

    return True
