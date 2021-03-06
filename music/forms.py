from django import forms
from .models import Album, Song
from django.contrib.auth.models import User


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file' ]
        widgets = {
            'album': forms.HiddenInput,
        }

