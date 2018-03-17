from django import forms
from django.utils.translation import gettext_lazy as _

from app.models import Channel, SubmittedPlaylist


class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        super(MultiWidgetBasic, self).__init__([forms.TextInput()], attrs)

    def decompress(self, value):
        if not value:
            return ''

        import json

        data = json.loads(value)
        json_values = list(data.keys())  # ALL JSON VALUES
        count = len(json_values)

        self.widgets = [forms.TextInput(attrs={'placeholder': str(key)}) for key in data]

        return [data[json_values[n]] for n in range(count)]


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
