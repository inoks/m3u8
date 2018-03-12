from django import forms
from django.utils.translation import gettext_lazy as _

from app.models import Channel, SubmittedPlaylist


class ChannelUpdateForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = [
            'title',
            'group',
            'path',
            'hidden',
        ]


class ChannelCreateForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = [
            'title',
            'path',
            'group',
            'hidden',
        ]


class SubmittedPlaylistForm(forms.ModelForm):
    class Meta:
        model = SubmittedPlaylist
        fields = [
            'url',
            'file',
            'remove_existed'
        ]

    def clean(self):
        cleaned_data = super(SubmittedPlaylistForm, self).clean()
        url = cleaned_data.get("url")
        file = cleaned_data.get("file")

        if not url and not file:
            raise forms.ValidationError(_("You should provide either file or url to your m3u8 playlist"))

        if url and file:
            raise forms.ValidationError(_("You should provide either file or url to your m3u8 playlist, not both"))

        return cleaned_data
