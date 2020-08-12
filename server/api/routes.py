from flask import Flask, request, Response
from endpoints.twitter import twitter
from endpoints.spotify import spotify
from rs import rs, sentiment


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
    """Main playlist creation route. This route when given the proper parameters will call the necessary functions from the Spotify, Twitter and Watson API's to 
    follow the steps of the recommendation algorithm. """
    twitter_username = request.args.get('user')
    spotify_token = request.args.get('token')
    playlist_name = request.args.get('name')
    num_songs = 50
    
    sp = spotify.authenticate_spotify(spotify_token)
    
    username = sp.me()['id']
    
    data = spotify.get_all_songs(username, sp)
    
    data = spotify.get_music_features(data, sp)

    emotions = sentiment.get_sentiment(twitter_username)   

    per_song = sentiment.adjust_songs(emotions, num_songs)

    playlist = rs.playlist_rs(data, emotions, per_song, num_songs)  

    playlist = spotify.create_playlist(sp, playlist, playlist_name)
    
    if playlist:
        response = Response(playlist, 201)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    elif error:
        response = Response(Exception, 500)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = Response('Not Found', 404)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        


if __name__ == "__main__":
    app.run()
