from flask import Flask, request, Response
from endpoints.twitter import twitter
from endpoints.spotify import spotify
from rs import rs


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
    if twitter.validate_user_exists(username):
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
    num_songs = request.args.get('songs')
    num_songs = int(num_songs)
    
    tones = rs.get_tones(twitter_username)
    per_song = rs.adjust_songs(tones, num_songs)

    # RS Playlist
    sp = spotify.authenticate_spotify(spotify_token)
    username = sp.me()['id']
    song_data = spotify.get_all_songs(username, sp)
    
    #Testing get_recent_tracks() function here
    #song_data = spotify.get_recent_tracks(username, sp)

    song_data = spotify.get_tracks_with_features(song_data, sp)
    
    # List of Track ID's
    song_data = rs.playlist_rs(song_data, tones, per_song, num_songs)
    playlist = spotify.create_playlist(sp, song_data, playlist_name)
    
    response = Response(playlist, 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
