from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/')
def postsong(request):

    if request.method == "GET":
        return render(request, "postsong.html", context={
            'artists': models.Artist.objects.all(),
        })
    else:

        title = request.POST.get('title')
        artist = request.POST.get('artist')
        key = request.POST.get('key')
        tuning = request.POST.get('tuning')
        author = request.user

        artist_api_form = artist.lower().replace(" ", "-")

        try:
            response = requests.get(f"https://www.vagalume.com.br/{artist_api_form}/index.js")
            artist_data = response.json()
            response_artist = artist_data["artist"]["desc"]

            try:
                get_artist = models.Artist.objects.get(name=response_artist)
            except ObjectDoesNotExist:
                get_artist = models.Artist.objects.create(name=response_artist)
                get_artist.save()

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro ao buscar artista.")
            return redirect("postsong")

        try:
            request_song = requests.get("https://api.vagalume.com.br/search.php"
                                   + "?art=" + artist
                                   + "&mus=" + title
                                   + "&apikey={key}")

            song_data = request_song.json()
            response_song = (song_data["mus"][0]['name'])

            try:
                get_song = models.Song.objects.create(author=author, title=response_song, artist=get_artist, key=key, tuning=tuning)
                get_song.save()
            except:
                messages.error(request, f"Não é possivel criar cifra dessa música!")
                return redirect("postsong")

        except:
            messages.error(request, f"Erro ao buscar música.")
            return redirect("postsong")


        return redirect('postchord', song_id=get_song.id)

@login_required(login_url='/')
def postchord(request, song_id):

    song = models.Song.objects.get(id=song_id)

    try:
        requisicao = requests.get("https://api.vagalume.com.br/search.php"
                                  + "?art=" + song.artist.name
                                  + "&mus=" + song.title
                                  + "&apikey={key}")

        address_data = requisicao.json()

        lyric = address_data["mus"][0]["text"]
    except:
        return HttpResponse("Musica ou Artista nao encontrado")

    return render(request, 'postchord.html', context={
        'song': song,
        'lyric': lyric,
    })

@login_required(login_url='/')
def finally_post_chord(request, song_id):

    song = models.Song.objects.get(id=song_id)

    chords = request.GET.get('chords')
    description = request.GET.get('description')

    print(chords)
    print(description)

    models.Song.objects.filter(id=song_id).update(chords=chords, description=description)


    #except:
    #   return HttpResponse("ERRO NAO ESPERADO")

    return redirect('homepage')













