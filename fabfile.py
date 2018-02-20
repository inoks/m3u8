from contextlib import contextmanager

import os
from fabric.api import run, cd, env, prefix, put

env.hosts = ['m3u8.ru', ]
env.user = 'root'

BASE_PATH = '/var/django/playlist'

env.activate = 'source ENV/bin/activate'


@contextmanager
def virtualenv():
    with cd(BASE_PATH):
        with prefix(env.activate):
            yield


def deploy():
    with cd(BASE_PATH):
        run('git pull')
        put('playlist/production.py',
            os.path.join(BASE_PATH, 'playlist/production.py'))

        # Update Nginx configuration
        put('nginx.conf', '/etc/nginx/sites-enabled/m3u8.conf')
        run('nginx -t')
        run('nginx -s reload')

        with virtualenv():
            run('pip install -U -r requirements.txt')
            run('python ./manage.py makemigrations --merge')
            run('python ./manage.py migrate')
            run('python ./manage.py collectstatic --noinput')
            run('python ./manage.py clearsessions')
            run('cp supervisor.conf /etc/supervisor/conf.d/playlist.conf')
            run('supervisorctl restart playlist')
