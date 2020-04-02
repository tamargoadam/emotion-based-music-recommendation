from flask import Flask, request


app = Flask(__name__)


@app.route('/twitter-username', methods=['POST'])
def get_twitter_username():
    username = request.json.get('twitter_username')
    if username:
        return 'Done', 201


@app.route('/spotify-token', methods=['POST'])
def get_spotify_token():
    token = request.json.get('spotify_token')
    if token:
        return 'Done', 201


@app.route('/playlist')
def playlist():

    return playlist
