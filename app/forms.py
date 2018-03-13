from django import forms
from django.utils.translation import gettext_lazy as _

from app.models import Channel, SubmittedPlaylist


class ChannelCreateUpdateForm(forms.ModelForm):
    class Meta:

        model = Channel

        fields = [
            'title',
            'group',
            'path',
            'extra_data',
            'duration',
            'hidden'
        ]

        widgets = {
            'path': forms.Textarea({'cols': 50, 'rows': 1}),
            'extra_data': forms.Textarea({'cols': 50, 'rows': 5})
        }

        # labels = {
        #     'title': _('Title'),
        #     'group': _('Group'),
        #     'path': _('Path'),
        #
        # }


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
