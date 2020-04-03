class User(object):
    spotify_token: str
    twitter_username: str
    playlist: list = []

    def __init__(self, token, username):
        self.spotify_token = token
        self.twitter_username = username
