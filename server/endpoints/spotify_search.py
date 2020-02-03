from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import pprint

search_str = input("Enter search string: ")

with open("spotify_credentials.json", "r") as file:
    creds = json.load(file)

client_credentials_manager = SpotifyClientCredentials(client_id=creds['CLIENT_ID'], client_secret=creds['CLIENT_SECRET'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result = sp.search(search_str)
pprint.pprint(result)
