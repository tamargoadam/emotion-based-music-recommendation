from flask import Flask, request, jsonify, Response
from models.user import User
from endpoints.twitter.twitter import validate_user_exists
from endpoints.spotify.spotify import *


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
    new_user = User(spotify_token, twitter_username)
    # TODO: use new_user to generate playlist
    # playlist = generate_playlist(new_user)
    """BEGIN EXAMPLE PLAYLIST"""
    sp = authenticate_spotify(spotify_token)
    results = get_artists_top_tracks(sp, get_top_and_similar_artists(sp))
    results = get_tracks_with_features(results, sp)
    print('\nTOP TRACKS WITH FEATURES\n')
    for result in results:
        print('{0} - {1}'.format(result['artist'], result['name']))
    playlist = create_playlist(sp, results, "TEST")
    response = Response(playlist, 201)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
