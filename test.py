#from server.rs.rs import rs
from server.endpoints.spotify import spotify
from server.endpoints.twitter import twitter
from server.endpoints.watson import watson
from server.rs import rs 

#auth spotify
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
redirect_uri = 'https://localhost:8000/callback/'
        #http://localhost:8888/callback/
sp = spotify.get_user_token('timdoozie', scope, redirect_uri)

#auth twitter
twitter_name = 'timdoozy'
num_songs = 50

#sentiment
tones = rs.get_tones(twitter_name)
#song per emotion type
per_song = rs.adjust_songs(tones, num_songs)

#spotify token
sp = spotify.authenticate_spotify(sp)
song_data = spotify.get_all_songs(sp)
song_data = spotify.get_tracks_with_features(song_data, sp)
# List of Track ID's
song_data = rs(song_data, tones, per_song, num_songs)

playlist_name = "Emotion-Based Recommendation"
playlist = spotify.create_playlist(sp, song_data, playlist_name)

    