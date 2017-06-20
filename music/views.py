from django.views import generic
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import Album, Song


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'
    model = Album

    def get_queryset(self):

        return Album.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return redirect('account_login')
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo', 'user']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class FavAlbum(View):
    def post(self, request, **kwargs):
        album = Album.objects.get(pk=self.kwargs['pk'])
        album.is_favorite = not album.is_favorite
        album.save()
        return HttpResponseRedirect(reverse_lazy('music:index'))


class SongView(generic.ListView):
    template_name = 'music/song.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        song_pk_list = []

        try:
            for album in Album.objects.filter(user=self.request.user):
                for song in album.song_set.all():
                    song_pk_list.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_pk_list)
        except Album.DoesNotExist:
            users_songs = []

        return users_songs

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return redirect('account_login')
        else:
            return super(SongView, self).dispatch(request, *args, **kwargs)


class SongCreate(CreateView):
    template_name = 'music/song_form.html'
    model = Song
    fields = ['song_title', 'audio_file']

    def form_valid(self, form):
        form.instance.album_id = self.kwargs.get('pk')
        return super(SongCreate, self).form_valid(form)


class SongUpdate(UpdateView):
    template_name = 'music/song_form.html'
    model = Song
    fields = ['song_title', 'audio_file']

    def form_valid(self, form):
        form.instance.album_id = self.kwargs.get('pk')
        return super(SongUpdate, self).form_valid(form)


class SongDelete(DeleteView):
    def post(self, request, **kwargs):
        album_id = self.kwargs['album_id']
        song = Song.objects.get(pk=self.kwargs['song_id']).delete()
        success_url = reverse_lazy('music:detail', kwargs={'pk': album_id})
        return HttpResponseRedirect(success_url)


class SongFavorite(View):
    def post(self, request, **kwargs):
        album_id = self.kwargs['album_id']
        song = Song.objects.get(pk=self.kwargs['song_id'])
        song.is_favorite = not song.is_favorite
        song.save()
        success_url = reverse_lazy('music:detail', kwargs={'pk': album_id})
        return HttpResponseRedirect(success_url)
