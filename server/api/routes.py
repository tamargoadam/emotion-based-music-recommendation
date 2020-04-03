from flask import Flask, request, jsonify
from models.user import User
from endpoints.twitter.twitter import validate_user_exists


app = Flask(__name__)


@app.route('/')
def default():
    return 'Found', 201


@app.route('/twitter-username')
def get_twitter_username():
    # example url extension: '/twitter-username?user=atamargo'
    username = request.args.get('user')
    if not username:
        return 'No username provided.', 400
    if validate_user_exists(username):
        return 'User, ' + username + ', validated successfully.', 201
    else:
        return 'User, ' + username + ', is not a valid user.', 400


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    """
    Data format should be as follows:
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
