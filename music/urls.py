from django.conf.urls import url
from . import views

app_name = 'music'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /music/pk/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # music/album/add/
    url(r'^album/add/$', views.AlbumCreate.as_view(), name='album_add'),
    url(r'^(?P<pk>[0-9]+)/favorite/$', views.FavAlbum.as_view(), name='favoritealbum'),
    # music/album/pk/
    url(r'^(?P<pk>[0-9]+)/update/$', views.AlbumUpdate.as_view(), name='album_update'),
    # music/album/pk/delete/
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album_delete'),
    url(r'^song/$', views.SongView.as_view(), name='songs'),
    # music/song/add/
    url(r'^(?P<pk>[0-9]+)/add/$', views.SongCreate.as_view(), name='song_add'),
    url(r'^(?P<album_id>[0-9]+)/song_delete/(?P<song_id>[0-9]+)$', views.SongDelete.as_view(), name='song_del'),
    url(r'^(?P<album_id>[0-9]+)/fav/(?P<song_id>[0-9]+)$', views.SongFavorite.as_view(), name='song_fav'),
]
