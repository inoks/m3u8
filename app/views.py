import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from app.forms import ChannelUpdateForm, ChannelCreateForm, SubmittedPlaylistForm
from app.models import Channel, Playlist
from app.utils import load_remote_m3u8, load_m3u8_from_file

logger = logging.getLogger(__name__)


class PublicPlaylistView(TemplateView):
    template_name = 'app/m3u8.txt'
    content_type = 'application/x-mpegURL'

    def get_context_data(self, **kwargs):
        context = super(PublicPlaylistView, self).get_context_data(**kwargs)
        playlist = get_object_or_404(Playlist, public_key=kwargs.get('public_key'))
        context['channels'] = playlist.channel_set.filter(hidden=False)
        return context

    def dispatch(self, *args, **kwargs):
        response = super(PublicPlaylistView, self).dispatch(*args, **kwargs)
        response['Content-Disposition'] = 'attachment; filename="list.m3u8"'
        return response


@method_decorator(login_required, name='dispatch')
class ChannelCreate(CreateView):
    model = Channel
    form_class = ChannelCreateForm

    def form_valid(self, form):
        playlist = Playlist.objects.filter(user=self.request.user).first()
        if not playlist:
            playlist = Playlist.objects.create(user=self.request.user)
        form.instance.playlist = playlist
        form.instance.user = self.request.user
        form.instance.save()

        form.instance.playlists.add(playlist)
        return super(ChannelCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ChannelUpdate(UpdateView):
    model = Channel
    form_class = ChannelUpdateForm

    def get_queryset(self):
        qs = super(ChannelUpdate, self).get_queryset().filter(user=self.request.user)
        return qs


@method_decorator(login_required, name='dispatch')
class ChannelList(ListView):
    model = Channel
    paginate_by = 50

    def get_queryset(self):
        qs = super(ChannelList, self).get_queryset().filter(user=self.request.user)
        group = self.request.GET.get('group')
        if group:
            qs = qs.filter(group=group)

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(group__icontains=q))

        order_by = self.request.GET.get('order_by')
        if order_by:
            qs = qs.order_by(order_by)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChannelList, self).get_context_data(**kwargs)
        playlist = Playlist.objects.filter(user=self.request.user).first()
        if not playlist:
            playlist = Playlist.objects.create(user=self.request.user)

        context['public_link'] = playlist.public_link

        return context


@method_decorator(login_required, name='dispatch')
class CreatePlaylist(CreateView):
    form_class = SubmittedPlaylistForm
    template_name = 'app/add_playlist.html'
    success_url = reverse_lazy('channels')

    def form_valid(self, form):
        playlist = Playlist.objects.filter(user=self.request.user).first()
        if not playlist:
            playlist = Playlist.objects.create(user=self.request.user)

        form.instance.user = self.request.user

        if form.cleaned_data['url']:
            load_remote_m3u8(
                form.cleaned_data['url'],
                playlist,
                remove_existed=form.cleaned_data['remove_existed'])
        elif form.cleaned_data['file']:
            load_m3u8_from_file(
                form.cleaned_data['file'],
                playlist,
                remove_existed=form.cleaned_data['remove_existed']
            )

        return super(CreatePlaylist, self).form_valid(form)


class IndexView(TemplateView):
    template_name = 'app/index.html'


@method_decorator(login_required, name='dispatch')
class ReactIndexView(TemplateView):
    template_name = 'app/react.html'
