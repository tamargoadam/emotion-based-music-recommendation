import json
from endpoints.spotify_helpers import *

username = input("Enter username: ")
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
redirect_url = 'https://localhost:8000'

with open("spotify_credentials.json", "r") as file:
    creds = json.load(file)

token = spotipy.util.prompt_for_user_token(username, scope, creds['CLIENT_ID'], creds['CLIENT_SECRET'], redirect_url)

if token:
    print("made it")
    sp = authenticate_spotify(token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for ", username)
