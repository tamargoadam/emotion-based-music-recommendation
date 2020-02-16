import spotipy
import random


def authenticate_spotify(token):
    """authenticates Spotify account via the passed in token"""
    print('...connecting to Spotify')
    sp = spotipy.Spotify(auth=token)
    return sp


def get_top_artists(sp: spotipy.Spotify):
    """compiles list of user's top artists"""
    print('...getting top artists')
    top_artists_name = []
    top_artists_uri = []
    ranges = ['short_term', 'medium_term', 'long_term']
    for r in ranges:
        all_top_artist_data = sp.current_user_top_artists(limit=50, time_range=r)
        top_artist_data = all_top_artist_data['items']
        for artist_data in top_artist_data:
            if artist_data['name'] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])
    return top_artists_uri


def get_artists_top_tracks(sp: spotipy.Spotify, top_artists_uri):
    """compiles unordered list of top tracks made by artists in top_artists_uri"""
    print('...getting top tracks for each artist')
    top_tracks_uri = []
    for artist in top_artists_uri:
        all_top_tracks_data = sp.artist_top_tracks(artist)
        top_tracks_data = all_top_tracks_data['tracks']
        for track_data in top_tracks_data:
            top_tracks_uri.append(track_data['uri'])
    random.shuffle(top_tracks_uri)
    return top_tracks_uri


def get_emo_tracks(sp: spotipy.Spotify, top_tracks_uri, emotion):
    """compile subset of top_tracks_uri that compliment indicated emotion"""
    return 0
