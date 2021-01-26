import spotipy
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import json
import numpy
import pandas as pd
from pandas import DataFrame


scope = 'user-top-read'
scope2= 'playlist-modify-public'
username='lldenisll'
token = SpotifyOAuth(scope=scope2, username=username)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp2 = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="0a273b88d8c343d1a8c087208fb86a26", client_secret="7867748d9abc48009a896c32637a9b33"))

sp3 = spotipy.Spotify(auth_manager=token)
# export SPOTIPY_CLIENT_ID=0a273b88d8c343d1a8c087208fb86a26
# export SPOTIPY_CLIENT_SECRET=7867748d9abc48009a896c32637a9b33
# export SPOTIPY_REDIRECT_URI=http://127.0.0.1:8081/
ranges = ['short_term', 'medium_term', 'long_term']
#ranges = ['long_term']
favorite_tracks_list = []
favorite_tracks_list_id = []
favorite_artist_list = []
tracks_for_add = []
genre_seeds = []

#Colecting five favorites in each range limited by 5 due to spotify api
for sp_range in ranges:
    results = sp.current_user_top_tracks(time_range=sp_range, limit=5)
    for i, item in enumerate(results['items']):
        favorite_tracks_list.append(item['name'])
        favorite_tracks_list_id.append(item['uri'])
        favorite_artist_list.append(item['artists'][0]['id'])

        # print(i, item['name'], '//', item['artists'][0]['name'])

#Getting 5 favorites for each range, and placing into one array 

favorite_tracks_list_id_short = favorite_tracks_list_id[:5]
favorite_tracks_list_id_medium = favorite_tracks_list_id[5:10]
favorite_tracks_list_id_long = favorite_tracks_list_id[10:15]


favorites_tracks = [favorite_tracks_list_id_short,favorite_tracks_list_id_medium,favorite_tracks_list_id_long]
           
#printing stuffs & getting info

print("Iremos criar uma playlist para você no seu Spotify")
print("Para isso iremos usar as suas musicas favoritas.. ")
print("...e alguns parâmetros, primeiro voce irá escolher 3 generos musicais, vamos lá!")
x=1
while x<=3:
    genre = input('Escolha 1 gênero musical: ')
    genre_seeds.append(genre)
    x+=1
acusticness= input('Digite de 0.1 até 1.0 o quão acústica você quer a playlist: ')
danceability= input('Digite de 0.1 até 1.0 o quão dançável você quer a playlist: ')
popularity= input('Digite de 1 até 100 o quão conhecida você quer a playlist: ')
songs_for_playlist =[]

for i in range(3):
    recommendated_songs = sp2.recommendations(seed_tracks=favorites_tracks[i],target_danceability=danceability ,target_acousticness=acusticness, target_popularity=popularity,limit=50)
    songs_for_playlist.append(recommendated_songs)

recommendated_songs_withou_seed = sp2.recommendations(target_danceability=danceability ,target_acousticness=acusticness, target_popularity=popularity, seed_genres=genre_seeds,limit=50)
songs_for_playlist.append(recommendated_songs_withou_seed)

for i in range(49):
    list_n=0
    while list_n <=3:
        tracks_for_add.append(songs_for_playlist[list_n]['tracks'][i]['uri'])
        list_n+=1

playlist_name = input("Digite o nome da playlist: ")
playlist_description = 'Playlist made by a robot using Python'
sp3.user_playlist_create(user=username, name=playlist_name,public=True, description=playlist_description)
pre_playlist= sp3.user_playlists(user=username)
playlist = pre_playlist['items'][0]['id']

sp3.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=tracks_for_add[:100])
sp3.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=tracks_for_add[101:199])



