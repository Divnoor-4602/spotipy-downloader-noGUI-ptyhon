import os
import spotipy
import youtube
from pprint import pprint
import requests
from spotipy.oauth2 import SpotifyOAuth

spotify_search_endpoint = "https://api.spotify.com/v1/search"
spotify_client_id = os.environ["CLIENT_ID"]
spotify_client_secret = os.environ["CLIENT_SECRET"]


def authorization():
    """performs spotify authorization"""
    sp_auth = SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="playlist-modify-private",
        cache_path="token.txt",
    )
    return sp_auth


def track_search(parameters, acc_token):
    """searches for the desired song over spotify and returns its uri id"""
    search_header = {"Authorization": f"Bearer {acc_token}"}
    search_req = requests.get(
        url=spotify_search_endpoint, params=parameters, headers=search_header
    )
    search_data = search_req.json()
    track_name = search_data["tracks"]["items"][0]["name"]
    track_artist = search_data["tracks"]["items"][0]["artists"][0]["name"]
    return track_name, track_artist


# spotify login
spotify_auth_obj = authorization()
access_token = spotify_auth_obj.get_access_token()[
    "access_token"
]  # gets the access token

# creates spotify client
spotify_client = spotipy.client.Spotify(oauth_manager=authorization())

# doing a search query
query_title = input("Enter name of the song ")
query_artist = input("Enter name of the artist ")
query_complete = f"track:{query_title} artist:{query_artist}"
search_parameters = {"q": query_complete, "type": "track", "limit": 1}
track_name_spotify, track_artist_spotify = track_search(
    search_parameters, acc_token=access_token
)  # url of the track we want to download
youtube_search_query = f"{track_name_spotify} by {track_artist_spotify}"

search_results = youtube.youtube_search(youtube_search_query)
print(search_results)

# downloading the track
track_to_save = youtube.youtube_download(
    query=search_results[0], track_name=track_name_spotify
)
