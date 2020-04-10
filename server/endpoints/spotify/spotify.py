import os
import spotipy
import random
import pandas as pd
import time


def get_user_token(username: str, scope: str, redirect_uri: str) -> str:
    """get token for specified user via credentials"""
    return spotipy.util.prompt_for_user_token(username, scope, os.environ['SPOTIFY_CLIENT_ID'],
                                              os.environ['SPOTIFY_CLIENT_SECRET'], redirect_uri)


def authenticate_spotify(token: str) -> spotipy.Spotify:
    """authenticates Spotify account via the passed in token"""
    print('...connecting to Spotify')
    sp = spotipy.Spotify(auth=token)
    return sp


def get_track_features(track_id: str, sp: spotipy.Spotify):
    """get dict of track features"""
    if track_id is None:
        return None
    else:
        features = sp.audio_features([track_id])
    return features


def get_tracks_with_features(tracks: list, sp: spotipy.Spotify) -> list:
    """return list of dicts with track info and features"""
    tracks_with_features = []
    for track in tracks:
        #print(track)
        features = get_track_features(track['id'], sp)
        if features:
            f = features[0]
            tracks_with_features.append(dict(
                                            id=track['id'],
                                            artist=track['artist'],
                                            name=track['name'],
                                            danceability=f['danceability'],
                                            instrumentalness=f['instrumentalness'],
                                            energy=f['energy'],
                                            loudness=f['loudness'],
                                            speechiness=f['speechiness'],
                                            acousticness=f['acousticness'],
                                            tempo=f['tempo'],
                                            liveness=f['liveness'],
                                            valence=f['valence']
                                            ))
    return tracks_with_features


def get_all_tracks_from_playlists(username: str, sp: spotipy.Spotify) -> list:
    print('...getting all tracks from playlists')
    playlists = sp.user_playlists(username)
    trackList = []
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print(playlist['name'], ' no. of tracks: ', playlist['tracks']['total'])
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


def get_top_and_similar_artists(sp: spotipy.Spotify, amount: int = 20) -> list:
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
    """compiles unordered list of top tracks made by artists in artists_uri of length amount"""
    print('...getting top tracks for each artist')
    tracks = []
    for artist in artists_uri:
        all_top_tracks_data = sp.artist_top_tracks(artist)
        top_tracks_data = all_top_tracks_data['tracks']
        for track_data in top_tracks_data:
            tracks.append(dict(id=track_data['id'], artist=track_data['artists'][0]['name'], name=track_data['name']))
            #tracks.append(track_data)
    #random.shuffle(tracks)
    #tracks = tracks[0:amount]
    return tracks


def create_playlist(sp: spotipy.Spotify, tracks: list, playlist_name: str, amount: int = 0):
    """creates a playlist or tracks from tracks_uri on the users account of length amount"""
    print('...creating playlist')
    if amount == 0:
        amount = len(tracks)
    user_id = sp.current_user()["id"]
    playlist_id = sp.user_playlist_create(user_id, playlist_name)["id"]
    random.shuffle(tracks)
    tracks_uri = []
    for track in tracks[0:amount]:
        tracks_uri.append(track['id'])
    sp.user_playlist_add_tracks(user_id, playlist_id, tracks_uri)
    print('playlist, {}, has been generated.'.format(playlist_name))
    return sp.playlist(playlist_id)["external_urls"]["spotify"]


def write_to_csv(track_features):
    df = pd.DataFrame(track_features)
    df.drop_duplicates(subset=['name', 'artist'])
    print('Total tracks in data set', len(df))
    df.to_csv('mySongsDataSet.csv', index=False)

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

def get_recent_tracks(username: str, sp: spotipy.Spotify) -> list:
    print('...getting the recent tracks from a user')
    recent_tracks = []
    afterTime = time.time()
    print(afterTime)
    #afterTime = afterTime - 2629743  #one month ago
    afterTime = afterTime - 604800 #one week ago
    print(afterTime)
    recent_tracks = sp.current_user_recently_played(after=afterTime)
    return recent_tracks

def get_all_songs(username: str, sp: spotipy.Spotify) -> list:
    #Method which gets songs from library, playlists, and top artists and similar artists into 1 dict
    print("Getting tracks from library...")
    trackList = [] #returning list
    #get all songs from playlists
    playlists = get_all_tracks_from_playlists(username, sp)
    #get all songs from library
    library = get_library(username, sp)
    #merge library and tracklist
    trackList = merge_dicts(playlists, library)
    #get all songs from top artists and similar artists
    preferences = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    #merge lists again
    trackList = merge_dicts(preferences, trackList)
    return trackList

def merge_dicts(list1: list, list2: list) -> list:
    #append two dictionaries together
    for item in list1:
        if item not in list2:
            list2.append(item)
    return list2

def get_library(username: str, sp: spotipy.Spotify) -> list:
    print("Getting tracks from user library..")
    trackList = []
    library = sp.current_user_saved_tracks()
    for item in library['items']:
        track = item['track']
        trackList.append(dict(id=track['id'], artist=track['artists'][0]['name'], name=track['name']))
    return trackList



"""
# TO TEST FUNCTIONS

username = 'atamargo'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
redirect_uri = 'https://localhost:8080/callback'

token = get_user_token(username, scope, redirect_uri)

if token:
    sp = authenticate_spotify(token)
    results = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    results = get_tracks_with_features(results, sp)
    print('\nTOP TRACKS WITH FEATURES\n')
    for result in results:
        print('{0} - {1}'.format(result['artist'], result['name']))
    create_playlist(sp, results, "TEST")
else:
    print("Can't get token for ", username)
"""
