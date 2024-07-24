import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import PrettyPrinter
import json

pp = PrettyPrinter()


# date = input("which year would you like to travel to, format is YYYY-MM-DD: \n")
date = "2000-10-01"
URL = f"https://www.billboard.com/charts/hot-100/{date}"

# use your own information!!
client_id = "client_id"  # use your own information!!
client_secret = "client_secret"  # use your own information!!
scope = "playlist-modify-private"



response = requests.get(url=URL)
# print(response.text)
soup = BeautifulSoup(response.text, "html.parser" )
song_titles = [tag.getText().strip() for tag in soup.select(selector="li ul li h3")]  # list
# print(song_titles)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth
    (
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://www.google.com",
        scope=scope,
        show_dialog=True,
        cache_path="token.txt"
    )
                    )
user_id = sp.current_user()["id"]
# print(sp.current_user())

year = "2000"
# song = "Could I Have This Kiss Forever"
songs_uris = []
for song in song_titles:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)   #  working, q的表达格式文档不清
        song_uri = result["tracks"]["items"][0]["uri"]
    except:  #有些歌找不到但是报错的时候是token，比较迷惑
        print(f"can not find {song}")
    else:
        songs_uris.append(song_uri)
# print(songs_uris)

# add a new play list
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=None)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id= playlist_id, items=songs_uris) # 成功










