from contextlib import contextmanager

import os
from fabric.api import run, cd, env, prefix, put
from fabric.context_managers import shell_env

env.hosts = ['m3u8.pzbz.ru', ]
env.user = 'root'

BASE_PATH = '/var/django/playlist'
DJANGO_SETTINGS_MODULE = 'project.production'

env.activate = 'source ENV/bin/activate'


@contextmanager
def virtualenv():
    with cd(BASE_PATH):
        with prefix(env.activate):
            yield


def deploy():
    with cd(BASE_PATH):
        run('git pull')
        put('project/production.py',
            os.path.join(BASE_PATH, 'project/production.py'))

        # Update Nginx configuration
        put('nginx.conf', '/etc/nginx/sites-enabled/m3u8.conf')
        run('nginx -t')
        run('nginx -s reload')

        with shell_env(DJANGO_SETTINGS_MODULE=DJANGO_SETTINGS_MODULE):
            with virtualenv():
                run('pip install -U pip')
                run('pip install -U -r requirements.txt')
                run('python ./manage.py migrate')
                run('python ./manage.py collectstatic --noinput')
                run('python ./manage.py clearsessions')
                run('cp supervisor.conf /etc/supervisor/conf.d/playlist.conf')
                run('supervisorctl restart playlist')


def deploy_frontend():
    with cd(BASE_PATH):
        run('git pull')

    # Deploy React frontend
    with cd('%s/frontend' % BASE_PATH):
        run('npm install')
        run('npm run build')
    with shell_env(DJANGO_SETTINGS_MODULE=DJANGO_SETTINGS_MODULE):
        with virtualenv():
            run('python ./manage.py collectstatic --noinput')
