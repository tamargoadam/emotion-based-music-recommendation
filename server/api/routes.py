from flask import Flask, request, jsonify, Response
from models.user import User
from endpoints.twitter.twitter import validate_user_exists


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


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    """
    get JSON user data, generate playlist for user, and post generated playlist.
    data format should be as follows:
    {
        "user" : {
            "spotify_token" : "my-token",
            "twitter_username" : "my-username"
            }
    }
    """
    user_data = request.json.get('user')
    new_user = User(user_data['spotify_token'], user_data['twitter_username'])
    playlist = []
    # TODO: use new_user to generate playlist
    # playlist = generate_playlist(new_user)
    return jsonify(playlist), 201


if __name__ == "__main__":
    app.run()
