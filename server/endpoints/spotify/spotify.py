import spotipy
import random
import json


def get_user_token(username: str, scope: str, redirect_uri: str):
    """get token for specified user via credentials"""
    with open("./spotify/spotify_credentials.json", "r") as file:
        creds = json.load(file)
    return spotipy.util.prompt_for_user_token(username, scope, creds['CLIENT_ID'], creds['CLIENT_SECRET'],
                                              redirect_uri)


def authenticate_spotify(token: str):
    """authenticates Spotify account via the passed in token"""
    print('...connecting to Spotify')
    sp = spotipy.Spotify(auth=token)
    return sp


def get_top_artists(sp: spotipy.Spotify, amount: int = 20):
    """compiles list of user's top artists of length amount"""
    print('...getting top artists')
    artists_name = []
    artists_uri = []
    ranges = ['short_term', 'medium_term', 'long_term']
    for r in ranges:
        all_top_artist_data = sp.current_user_top_artists(limit=amount, time_range=r)
        top_artist_data = all_top_artist_data['items']
        for artist_data in top_artist_data:
            if artist_data['name'] not in artists_name:
                artists_name.append(artist_data['name'])
                artists_uri.append(artist_data['uri'])
    return artists_uri


def get_top_and_similar_artists(sp: spotipy.Spotify, amount: int = 20):
    """compiles a list of top and similar artists of length amount"""
    print('...getting top and similar artists')
    artists_name = []
    artists_uri = []
    ranges = ['short_term', 'medium_term', 'long_term']
    for r in ranges:
        all_top_artist_data = sp.current_user_top_artists(limit=amount, time_range=r)
        top_artist_data = all_top_artist_data['items']
        for artist_data in top_artist_data:
            if artist_data['name'] not in artists_name and len(artists_uri) < amount:
                artists_name.append(artist_data['name'])
                artists_uri.append(artist_data['uri'])
                similar_artists_data = sp.artist_related_artists(artist_id=artist_data['uri'])
                for index, similar_artist_data in enumerate(similar_artists_data['artists']):
                    if similar_artist_data['name'] not in artists_name and len(artists_uri) < amount:
                        artists_name.append(similar_artist_data['name'])
                        artists_uri.append(similar_artist_data['uri'])
                    if index == 2:
                        break
    return artists_uri


def get_artists_top_tracks(sp: spotipy.Spotify, artists_uri: list, amount: int = 50):
    """compiles unordered list of top tracks made by artists in artists_uri of length amount"""
    print('...getting top tracks for each artist')
    tracks_uri = []
    for artist in artists_uri:
        all_top_tracks_data = sp.artist_top_tracks(artist)
        top_tracks_data = all_top_tracks_data['tracks']
        for track_data in top_tracks_data:
            tracks_uri.append(track_data['uri'])
    random.shuffle(tracks_uri)
    tracks_uri = tracks_uri[0:amount]
    return tracks_uri


def get_emo_tracks(sp: spotipy.Spotify, top_tracks_uri: list, emotion: list):
    """compile subset of top_tracks_uri that compliment indicated emotion"""
    return


def create_playlist(sp: spotipy.Spotify, tracks_uri: list, playlist_name: str, amount: int = 0):
    """creates a playlist or tracks from tracks_uri on the users account of length amount"""
    print('...creating playlist')
    if amount == 0:
        amount = len(tracks_uri)
    user_id = sp.current_user()["id"]
    playlist_id = sp.user_playlist_create(user_id, playlist_name)["id"]
    random.shuffle(tracks_uri)
    sp.user_playlist_add_tracks(user_id, playlist_id, tracks_uri[0:amount])
    print('playlist, {}, has been generated.'.format(playlist_name))


username = input("Enter username: ")
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
redirect_uri = 'https://localhost:8000/callback'

token = get_user_token(username, scope, redirect_uri)

if token:
    sp = authenticate_spotify(token)
    results = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    """print('\nTOP TRACKS\n')
    for uri in results:
        track = sp.track(uri)
        print(track['name'])"""
    create_playlist(sp, results, "TEST")
else:
    print("Can't get token for ", username)
