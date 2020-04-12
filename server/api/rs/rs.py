from endpoints.watson import watson
from endpoints.twitter import twitter
from endpoints.spotify import spotify
import pandas as pd
import random
import os
import math

#
# RS.py
# rs(twitter_name, spotify_name, num_songs)
#   returns a list of song ids to be used for populating a new playlist
    #rs func
""" 
def rs_playlist(twitter_name: str, spotify_name: str, num_songs: int):
    # Method to call when a user needs a new playlist created based on the number of songs as input
    
    #sentiment scores
    tones = get_tones(twitter_name) # {'joy': 0.617353, 'anger': 0.542552}
    #tones = watson.sort_tones(tones)
    #print(tones)
    #songs per emotion to be added to playlist
    per_song = adjust_songs(tones, num_songs) # {'anger': 24, 'joy': 26}
    
    #get spotify auth
    scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
    redirect_uri = 'https://localhost:8000/callback'
    token = spotify.get_user_token(spotify_name, scope, redirect_uri) #spotify.
    if token:
        print('Success, got spotify token')
    else:
        print("Cant get token for ", spotify_name)
    sp = spotify.authenticate_spotify(token) #spotify.
    feature_data = spotify.get_all_songs(spotify_name, sp) #spotify.
    feature_data = spotify.get_tracks_with_features(feature_data, sp) #spotify.
"""      
def playlist_rs(feature_data, tones, per_song, num_songs):
    # list of track ids to be added to a playlist at the end of the algorithm
    playlist_tracks = []  
    
    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    #all_tracks 
    all_tracks = df.copy() 
    all_tracks = all_tracks.drop(['speechiness','instrumentalness','liveness','acousticness','name','artist','loudness','tempo','danceability'], axis=1)
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)

    #joy_tracks
    joy_tracks = df.copy()
    joy_tracks = joy_tracks.drop(['speechiness','instrumentalness','liveness','acousticness','name','artist','loudness','tempo','danceability'], axis=1)
    joy_tracks = joy_tracks[joy_tracks['energy'] > 0.5]
    joy_tracks = joy_tracks[joy_tracks['valence'] > 0.5]
    #shuffle joy_tracks
    joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True)

    #anger_tracks
    anger_tracks = df.copy()
    anger_tracks = anger_tracks.drop(['speechiness','instrumentalness','liveness','acousticness','name','artist','loudness','tempo','danceability'], axis=1)
    anger_tracks = anger_tracks[anger_tracks['energy'] > 0.5]
    anger_tracks = anger_tracks[anger_tracks['valence'] < 0.5]
    #shuffle anger_tracks
    anger_tracks = anger_tracks.sample(frac=1).reset_index(drop=True)

    #sad_tracks
    sad_tracks = df.copy()
    sad_tracks = sad_tracks.drop(['speechiness','instrumentalness','liveness','acousticness','name','artist','loudness','tempo','danceability'], axis=1)
    sad_tracks = sad_tracks[sad_tracks['energy'] < 0.5]
    sad_tracks = sad_tracks[sad_tracks['valence'] < 0.5]
    #shuffle sad_tracks
    sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
    
    #calm_tracks
    calm_tracks = df.copy()
    calm_tracks = calm_tracks.drop(['speechiness','instrumentalness','liveness','acousticness','name','artist','loudness','tempo','danceability'], axis=1)
    calm_tracks = calm_tracks[calm_tracks['energy'] < 0.5]
    calm_tracks = calm_tracks[calm_tracks['valence'] > 0.5]
    #shuffle calm_tracks
    calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)

    #check what tones have been calculated
    tone_scores = [0, 0, 0, 0]
    songs_per_tone = [0, 0, 0, 0]
                #joy[0],anger[1],sadness[2],calm[3]

    #fill tone_scores
    if 'joy' in tones.keys():
        tone_scores[0] = tones['joy']
    if 'anger' in tones.keys():
        tone_scores[1] = tones['anger']
    if 'sadness' in tones.keys():
        tone_scores[2] = tones['sadness']
    if 'calm' in tones.keys():
        tone_scores[3] = tones['calm']

    #fill tone_songs
    if 'joy' in per_song.keys():
        songs_per_tone[0] = per_song['joy']
    if 'anger' in per_song.keys():
        songs_per_tone[1] = per_song['anger']
    if 'sadness' in per_song.keys():
        songs_per_tone[2] = per_song['sadness']
    if 'calm' in per_song.keys():
        songs_per_tone[3] = per_song['calm']
    
    #loop, only decrementing the counter when a song is added to playlist__tracks list of ids
    count1 = num_songs
    while(count1 > 0):
        for i in range(len(tone_scores)):   #repeatedly loop through each song type
            if songs_per_tone[i] == 0: #no songs to add of this emotion
                i += 1      # skip to next song type in list
            elif songs_per_tone[i] > 0 and i == 0:
                # joy song to be added to playlist
                temp_song = joy_tracks.at[0, 'id']
                # CHECK IF ITS ALREADY IN PLAYLIST!!!!
                if temp_song not in playlist_tracks:
                    #if its not in playlist, then add it to playlist!
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                # if its in the playlist or not, either way we must now shuffle and drop that element and keep looping
                joy_tracks.drop(0)
                joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True)
                # Subtract from count1
                count1 -= 1

            elif songs_per_tone[i] > 0 and i == 1:
                # anger song to be added to playlist
                temp_song = anger_tracks.at[0, 'id']
                # CHECK IF ITS ALREADY IN PLAYLIST!!!!
                if temp_song not in playlist_tracks:
                    #if its not in playlist, then add it to playlist!
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                # if its in the playlist or not, either way we must now shuffle and drop that element and keep looping
                anger_tracks.drop(0)
                anger_tracks = anger_tracks.sample(frac=1).reset_index(drop=True)
                # Subtract from count1
                count1 -= 1
                
            elif songs_per_tone[i] > 0 and i == 2:
                # sad song to be added to playlist
                temp_song = sad_tracks.at[0, 'id']
                # CHECK IF ITS ALREADY IN PLAYLIST!!!!
                if temp_song not in playlist_tracks:
                    #if its not in playlist, then add it to playlist!
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                # if its in the playlist or not, either way we must now shuffle and drop that element and keep looping
                sad_tracks.drop(0)
                sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
                # Subtract from count1
                count1 -= 1
                
            elif songs_per_tone[i] > 0 and i == 3:
                # calm song to be added to playlist
                temp_song = calm_tracks.at[0, 'id']
                # CHECK IF ITS ALREADY IN PLAYLIST!!!!
                if temp_song not in playlist_tracks:
                    #if its not in playlist, then add it to playlist!
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                # if its in the playlist or not, either way we must now shuffle and drop that element and keep looping
                calm_tracks.drop(0)
                calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)
                # Subtract from count1
                count1 -= 1
            
            elif (songs_per_tone[0] == 0) and (songs_per_tone[1] == 0) and (songs_per_tone[2] == 0) and (songs_per_tone[3] == 0):
                #there are no emotion songs left to be added to the playlist
                #fill the rest of the playlist with preferred songs randomly
                temp_song = all_tracks.at[0, 'id']
                if temp_song not in playlist_tracks:
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                all_tracks.drop(0)
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
                count1 -= 1

    return playlist_tracks

    #create a playlist instead of returning the list of playlist tracks
    #out = spotify.create_playlist(sp, playlist_tracks, "Emotion-Based Recommendations")
    #return out
    
    
def get_tones(username: str) -> dict:
    """generate list of sentiments corresponding to user's tweets"""
    tweet_data = twitter.get_all_tweets(username)
    sentiment_data = watson.get_sentiment(tweet_data) #watson. twitter.
    sentiment_data = watson.format_sentiment(sentiment_data) #watson.
    sentiment_data = watson.sort_tones(sentiment_data)
    return sentiment_data

def adjust_songs(tone_in: dict, nums: int) -> dict:
    #Returns a new dictionary containing the amount of songs of each tone to produce in the playlist
    temp_calm = 0
    temp_joy = 0
    temp_anger = 0
    temp_sad = 0
    length = len(tone_in)
    song_num = nums

    count = 0
    div = 0
    if 'joy' in tone_in.keys():
        temp_joy = tone_in['joy']
        count = count + 1
    if 'anger' in tone_in.keys():
        temp_anger = tone_in['anger']
        count = count + 1
    if 'sadness' in tone_in.keys():
        temp_sad = tone_in['sadness']
        count = count + 1
    if 'calm' in tone_in.keys():
        temp_calm = tone_in['calm']
        count = count + 1

    if count > 0:
        div = 1 / count
    else: 
        div = 1
    sum1 = 0
    
    list_vals = [0, 0, 0, 0]
    #joy, anger, sad, calm
    
    #getsum1
    if temp_joy > 0:
        temp_joy *= song_num
        temp_joy *= div
        temp_joy = math.floor(temp_joy)
        list_vals[0] = temp_joy
        sum1 += temp_joy
    if temp_anger > 0:
        temp_anger *= song_num
        temp_anger *= div
        temp_anger = math.floor(temp_anger)
        list_vals[1] = temp_anger
        sum1 += temp_anger
    if temp_sad > 0:
        temp_sad *= song_num
        temp_sad *= div
        temp_sad = math.floor(temp_sad)
        list_vals[2] = temp_sad
        sum1 += temp_sad
    if temp_calm > 0:
        temp_calm *= song_num
        temp_calm *= div
        temp_calm = math.floor(temp_calm)
        list_vals[3] = temp_calm
        sum1 += temp_calm
    
    #show_vals(temp_sad, temp_joy, temp_anger, temp_calm)
    
    #showing vals for testing
    #for i in list_vals:
        #print(i)
        
    #sum1 vs song_num
    if sum1 < song_num:
        while sum1 < song_num:
            for i in range(len(list_vals)):
                if(list_vals[i] == 0):
                    i += 1
                else:
                    list_vals[i] = list_vals[i] + 1
                    sum1 += 1
    #highly unlikely sum1 > song_num
    if sum1 > song_num:
        print("ERROR: Exception, account for this case")
    
    #showing vals for testing    
    #for i in list_vals:
        #print(i)
        
    #list_val[joy, anger, sad, calm]
    ret_dic = tone_in.copy()
      
    #update the output dictionary with new values
    if 'joy' in ret_dic.keys():
        ret_dic['joy'] = list_vals[0]
    if 'anger' in ret_dic.keys():
        ret_dic['anger'] = list_vals[1]
    if 'sadness' in ret_dic.keys():
        ret_dic['sadness'] = list_vals[2]
    if 'calm' in ret_dic.keys():
        ret_dic['calm'] = list_vals[3]
        
    return ret_dic
    
    #function for testing
def show_vals(sad, joy, anger, calm):
    print("Sad: %d" %sad)
    print("Joy: %d" %joy)
    print("Anger: %d" %anger)
    print("Calm: %d" %calm)

