from django import forms
from django.utils.translation import gettext_lazy as _

from app.models import Channel, SubmittedPlaylist


class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput()]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            import json

            dictor = json.loads(value)
            keys = list(dictor.keys())

            return dictor[keys[0]], dictor[keys[1]]
        else:
            return '', ''


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
            'extra_data': MultiWidgetBasic()
        }


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
