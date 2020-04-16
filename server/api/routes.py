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

    # Getting Spotify Data
    sp = spotify.authenticate_spotify(spotify_token)
    username = sp.me()['id']
    song_data = spotify.get_all_songs(username, sp) # Call -> Get all songs from a user's spotify account
                                                    # Top Artist Tracks, Top Similiar Artist Tracks, Recent Tracks (Last 3-7 days?),
                                                    # Get saved songs from User's Library, Get saved tracks within a users saved playlists
    song_data = spotify.get_tracks_with_features(song_data, sp) # Call -> get the feature data for each song 
                                                                # PROBLEM: Efficiency of this call is O(N)
                                                                # It gets feature data 1 song at a time from song_data
                                                                # SOLUTION: https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/

    # Sentiment Analysis
    tones = rs.get_tones(twitter_username)          # Call -> document tones
    per_song = rs.adjust_songs(tones, num_songs)    # Call -> songs per tone to be put in final playlist
    
    # RS Playlist generation algorithm call
    if len(tones) == 0 or len(per_song) == 0:
        # Then lets call the random_rs() playlist
        song_data = rs.random_rs(song_data, num_songs)
        playlist = spotify.create_playlist(sp, song_data, playlist_name)
        print("Generated random playlist due to insufficient sentiment data from twitter account")
    else:
        # Then there is sentiment data
        song_data = rs.playlist_rs(song_data, tones, per_song, num_songs) # Call -> playlist_rs() performs the arrangement of songs into the final playlist
        playlist = spotify.create_playlist(sp, song_data, playlist_name) # Call -> Save the playlist in the user's spotify library.
    
    response = Response(playlist, 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
