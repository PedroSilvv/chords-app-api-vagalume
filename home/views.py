from django.shortcuts import render
from postsong.models import Song, Artist

def home(request):
    return render(request, 'home.html', context={
        "user": request.user,
    })

def filter_song(request):

    if request.method == "POST":

        song = request.POST.get("song")
        artist_name = request.POST.get("artist")

        if artist_name:
            artist = Artist.objects.get(name=artist_name)

        songs_filter = Song.objects.all()

        if len(song) > 0 and len(artist_name) > 0:
            songs_filter = Song.objects.filter(title=song, artist=artist)

        if len(song) > 0 and len(artist_name) == 0:
            songs_filter = Song.objects.filter(title=song)

        if len(artist_name) > 0 and len(song) == 0:
            songs_filter = Song.objects.filter(artist=artist)

        return render(request, "songsfilter.html", context={
            "songs" : songs_filter,
        })