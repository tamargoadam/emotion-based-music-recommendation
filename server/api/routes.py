from flask import Flask, request, jsonify, Response
from server.endpoints.twitter import validate_user_exists
from server.endpoints.spotify import spotify
#from endpoints.watson.watson import watson
from server.endpoints.watson import watson
from server.rs import rs

app = Flask(__name__)


@app.route('/')
def default():
    """default server url"""
    return 'Found', 201


@app.route('/twitter-username')
def get_twitter_username():
    """
    validates that argument, user, is a valid twitter username.
    example url extension: '/twitter-username?user=atamargo'
    """
    username = request.args.get('user')
    if not username:
        response = Response('No username provided.', 400)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    if validate_user_exists(username):
        response = Response(username, 201)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = Response('User, ' + username + ', is not a valid user.', 403)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route('/playlist')
def playlist():
    twitter_username = request.args.get('user')
    spotify_token = request.args.get('token')
    playlist_name = request.args.get('name')
    
    # RS
    #num_songs = request.args.get('num_songs')
    num_songs = 50

    tones = rs.get_tones(twitter_username)
    per_song = rs.adjust_songs(tones, num_songs)

    # RS Playlist
    sp = spotify.authenticate_spotify(spotify_token)
    song_data = spotify.get_all_songs(sp)
    song_data = spotify.get_tracks_with_features(song_data, sp)
    # List of Track ID's
    song_data = rs(song_data, tones, per_song, num_songs)
    playlist = spotify.create_playlist(sp, song_data, playlist_name)

    

    """BEGIN EXAMPLE PLAYLIST PLACEHOLDER
    sp = authenticate_spotify(spotify_token)
    results = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    results = get_tracks_with_features(results, sp)
    print('\nTOP TRACKS WITH FEATURES\n')
    for result in results:
        print('{0} - {1}'.format(result['artist'], result['name']))
    playlist = create_playlist(sp, results, playlist_name)
    END EXAMPLE PLAYLIST PLACEHOLDER"""

    response = Response(playlist, 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
