import os
import spotipy
import random
import pandas as pd


def get_user_token(username: str, scope: str, redirect_uri: str) -> str:
    # get token for specified user via credentials
    return spotipy.util.prompt_for_user_token(username, scope, os.environ['SPOTIFY_CLIENT_ID'],
                                              os.environ['SPOTIFY_CLIENT_SECRET'], redirect_uri)


def authenticate_spotify(token: str) -> spotipy.Spotify:
    # authenticates Spotify account via the passed in token
    print('...connecting to Spotify')
    sp = spotipy.Spotify(auth=token)
    return sp


def get_all_songs(username: str, sp: spotipy.Spotify) -> list:
    """The get_all_songs() function is the parent function for retrieving as many songs from a spotify user as possible.
    It will make a call for each of the different methods of retrieving tracks from a user's account and then use 
    a helper function to merge the dictionaries. The resulting output is a list of dictionaries of tracks upwards of 1000. """
    tracks = []

    playlists = get_all_tracks_from_playlists(username, sp)

    tracks = get_library(username, sp)

    tracks = merge_dicts(playlists, tracks)

    preferences = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    tracks = merge_dicts(preferences, tracks)
    
    recents = get_recent_tracks(username, sp)
    tracks = merge_dicts(recents, tracks)

    recentArtists = get_recent_artists(username, sp)
    recentArtists = get_artists_top_tracks(sp, recentArtists)
    tracks = merge_dicts(recentArtists, tracks)
    
    return tracks

def get_music_features(tracks, sp):
    """This function will take a list of tracks and request the audio features from Spotify for 100 tracks at a time.
    This is to improve efficiency from the previous iteration, where a separate api call would be made for individual tracks. """
    track_features = []

    track_list = []
    for i in range(len(tracks)):
        track_list.append(tracks[i]['id'])
    
    num_tracks = len(tracks)
    for i in range(0, num_tracks, 100):
        if i + 100 > num_tracks:
            features = track_list[i:num_tracks]
            features = sp.audio_features(features)
            for j in range(len(features)):
                track_features.append({'id': features[j]['id'], 'energy': features[j]['energy'], 'valence': features[j]['valence']})
        else:
            features = track_list[i:i+100]
            features = sp.audio_features(features)
            for j in range(len(features)):
                track_features.append({'id': features[j]['id'], 'energy': features[j]['energy'], 'valence': features[j]['valence']})
    
    return track_features


def get_all_tracks_from_playlists(username: str, sp: spotipy.Spotify) -> list:
    print('...getting all tracks from playlists')
    playlists = sp.user_playlists(username)
    trackList = []
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            for i, item in enumerate(tracks['items']):
                track = item['track']
                trackList.append(dict(id=track['id'], artist=track['artists'][0]['name'], name=track['name']))
    return trackList


def get_top_artists(sp: spotipy.Spotify, amount: int = 20) -> list:
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


def get_top_and_similar_artists(sp: spotipy.Spotify, amount: int = 30) -> list:
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


def get_artists_top_tracks(sp: spotipy.Spotify, artists_uri: list, amount: int = 50) -> list:
    # compiles list of top tracks made by artists in artists_uri of length amount
    print('...getting top tracks for each artist')
    tracks = []
    for artist in artists_uri:
        all_top_tracks_data = sp.artist_top_tracks(artist)
        top_tracks_data = all_top_tracks_data['tracks']
        for track_data in top_tracks_data:
            tracks.append(dict(id=track_data['id'], artist=track_data['artists'][0]['name'], name=track_data['name']))
    return tracks


def create_playlist(sp: spotipy.Spotify, tracks: list, playlist_name: str):
    """creates a playlist or tracks from tracks_uri on the users account of length amount"""
    print('...creating playlist')
    user_id = sp.current_user()["id"]
    playlist_id = sp.user_playlist_create(user_id, playlist_name)["id"]
    random.shuffle(tracks)
    tracks_uri = []
    for track in tracks:
        tracks_uri.append(track)
    sp.user_playlist_add_tracks(user_id, playlist_id, tracks_uri)
    print('playlist, {}, has been generated.'.format(playlist_name))
    return sp.playlist(playlist_id)["external_urls"]["spotify"]


def get_recent_tracks(username: str, sp: spotipy.Spotify) -> list:
    print('...getting the recent tracks from a user')
    ret = []
    recent_tracks = sp.current_user_recently_played()
    for item in recent_tracks['items']:
        track = item['track']
        ret.append(dict(id=track['id'], artist=track['artists'][0]['name'], name=track['name']))
    return ret


def get_recent_artists(username: str, sp: spotipy.Spotify) -> list:
    print('...getting the artists from recent user songs played')
    artists_uri = []
    recent_artists = sp.current_user_recently_played()
    for item in recent_artists['items']:
        track = item['track']
        for artist in track['artists']:
            if artist['uri'] not in artists_uri:
                artists_uri.append(artist['uri'])
    return artists_uri


def merge_dicts(list1: list, list2: list) -> list:
    # append two dictionaries together
    for item in list1:
        if item not in list2:
            list2.append(item)
    return list2


def get_library(username: str, sp: spotipy.Spotify) -> list:
    print("...getting tracks from user library")
    trackList = []
    library = sp.current_user_saved_tracks()
    for item in library['items']:
        track = item['track']
        trackList.append(dict(id=track['id'], artist=track['artists'][0]['name'], name=track['name']))
    return trackList

