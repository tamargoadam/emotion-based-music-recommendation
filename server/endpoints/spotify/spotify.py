import spotipy
import random
import json
import pandas as pd


def get_user_token(username: str, scope: str, redirect_uri: str):
    """get token for specified user via credentials"""
    with open("../credentials/spotify_credentials.json", "r") as file:
        creds = json.load(file)
    return spotipy.util.prompt_for_user_token(username, scope, creds['CLIENT_ID'], creds['CLIENT_SECRET'],
                                              redirect_uri)


def authenticate_spotify(token: str):
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


def get_tracks_with_features(tracks: list, sp: spotipy.Spotify):
    """return list of dicts with track info and features"""
    tracks_with_features = []

    for track in tracks:
        print(track)
        features = get_track_features(track['id'], sp)
        if features:
            f = features[0]
            tracks_with_features.append(dict(
                                            name=track['name'],
                                            artist=track['artists'][0]['name'],
                                            id=track['id'],
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


def get_all_tracks_from_playlists(username: str, sp: spotipy.Spotify):
    """saves %s_music.csv a collection of all songs with feature data"""
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
                trackList.append(dict(name=track['name'], id=track['id'], artist=track['artists'][0]['name']))
    return trackList


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
    tracks = []
    for artist in artists_uri:
        all_top_tracks_data = sp.artist_top_tracks(artist)
        top_tracks_data = all_top_tracks_data['tracks']
        for track_data in top_tracks_data:
            tracks.append(track_data)
    random.shuffle(tracks)
    tracks = tracks[0:amount]
    return tracks


def get_emo_tracks(sp: spotipy.Spotify, top_tracks_uri: list, emotion: list):
    """compile subset of top_tracks_uri that compliment indicated emotion"""
    return


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
        tracks_uri.append(track['uri'])
    sp.user_playlist_add_tracks(user_id, playlist_id, tracks_uri)
    print('playlist, {}, has been generated.'.format(playlist_name))


def write_to_csv(track_features):
    df = pd.DataFrame(track_features)
    df.drop_duplicates(subset=['name', 'artist'])
    print('Total tracks in data set', len(df))
    df.to_csv('mySongsDataSet.csv', index=False)


"""
# TO TEST FUNCTIONS

username = 'atamargo'
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
redirect_uri = 'https://localhost:8000/callback'

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
