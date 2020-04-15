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
    num_songs = int(num_songs) # We want num_songs to be in range (25-100)
    # CHECK IF NUM_SONGS IS IN RANGE 25-100
    
    # Sentiment Analysis
    tones = rs.get_tones(twitter_username)  # Call 1 -> document tones
        # if tones returns an empty dictionary it will be accounted for in playlist_rs() function call
    per_song = rs.adjust_songs(tones, num_songs) # Call 2 -> songs per tone to be put in final playlist
        # if tones returns an empty dictionary, so will per_song

    # Getting Spotify Data
    sp = spotify.authenticate_spotify(spotify_token)
    username = sp.me()['id']
    song_data = spotify.get_all_songs(username, sp) # Call 3 -> Get all songs from a user's spotify account
                                                    # Top Artist Tracks, Top Similiar Artist Tracks, Recent Tracks (Last 3-7 days?),
                                                    # Get saved songs from User's Library, Get saved tracks within a users saved playlists
    song_data = spotify.get_tracks_with_features(song_data, sp) # Call 4 -> get the feature data for each song 
                                                                # PROBLEM: Efficiency of this call is O(N)
                                                                # It gets feature data 1 song at a time from song_data
                                                                # SOLUTION: https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/

    # List of Track ID's
    song_data = rs.playlist_rs(song_data, tones, per_song, num_songs) # Call 5 -> playlist_rs() performs the arrangement of songs into the final playlist
    playlist = spotify.create_playlist(sp, song_data, playlist_name) # Call 6 -> Save the playlist in the user's spotify library.
    
    response = Response(playlist, 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
