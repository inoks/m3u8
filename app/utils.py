import logging
import random
import string



import requests
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


def generate_random_key(length=4):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def extinf_format(fo, playlist):
    from app.models import Channel
    # import re
    import m3u8

    fo.file.seek(0)
    content = fo.read().decode('utf-8')

    all = m3u8.loads(content)

    for segment in all.segments:

        Channel.objects.create(
            playlist=playlist,
            title=segment.title if segment.title else None,
            duration=segment.duration if segment.duration else None,
            group=segment.group if hasattr(segment, 'group') else None,
            path=segment.uri
        )

    # duration = re.search(r'EXTINF:(?P<duration>-?\d+)', content)
    #
    # group_title = re.search(r'group-title=(?P<group_title>".+")', content)
    #
    # http = re.search(r'(?P<group_title>((http|https):\/\/).+$)', content)
    #
    # title = re.search(r',(?P<group_title>.*) ', content)

    # tvg_id = re.search(rb'tvg-id=(?P<tvg_id>"[^`"]+")', content)

    # tvg_name = re.search(rb'tvg-name=(?P<tvg_name>".+")', content)

    # tvg_logo = re.search(rb'tvg-logo=(?P<tvg_logo>"[^`"]+")', content)

    # tvg_country = re.search(rb'tvg-country=(?P<group_title>"[^`"]+")', content)

    # tvg_language = re.search(rb'tvg-language=(?P<group_title>"[^`"]+")', content)

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
            duration, title = line[8:].split(',')
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
    import m3u8

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

    duration = title = group = None

    all = m3u8.loads(content)

    if all.segments:
        for segment in all.segments:
            Channel.objects.create(
                playlist=playlist,
                title=segment.title if segment.title else None,
                duration=segment.duration if segment.duration else None,
                group=segment.group if hasattr(segment, 'group') else None,
                path=segment.uri
            )

    # for line in fo.read().splitlines():
    #     line = line.decode("utf-8")
    #
    #     if line == '#EXTM3U':
    #         continue
    #
    #     if line.startswith('#EXTINF:'):
    #         duration, title = line[8:].split(',')
    #         continue
    #
    #     if line.startswith('#EXTGRP:'):
    #         group = line[8:]
    #         continue
    #
    #     if line.startswith('#'):
    #         logger.warning('Unsupported line skipped: {}'.format(line))
    #         continue
    #
    #     if line:
    #         path = line
    #
    #         Channel.objects.create(
    #             playlist=playlist,
    #             title=title,
    #             duration=duration,
    #             group=group,
    #             path=path
    #         )
