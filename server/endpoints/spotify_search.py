import json
from endpoints.spotify_helpers import *

username = input("Enter username: ")
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
redirect_url = 'https://localhost:8000'

with open("spotify_credentials.json", "r") as file:
    creds = json.load(file)

token = spotipy.util.prompt_for_user_token(username, scope, creds['CLIENT_ID'], creds['CLIENT_SECRET'], redirect_url)

if token:
    sp = authenticate_spotify(token)
    results = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    print('\nTOP TRACKS\n')
    for uri in results:
        track = sp.track(uri)
        print(track['name'])
else:
    print("Can't get token for ", username)
