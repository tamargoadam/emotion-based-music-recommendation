from endpoints import watson, twitter
import pandas as pd
import math

""" 
This file contains the necessary recommendation algorithms which identify and suggest the final songs to be added to new playlists. The following emotional mapping between music features and 
emotion are estimated with Thayers 2D Emotional Model. 
"""

def playlist_rs(feature_data, tones, per_song, num_songs):
    """This is the main playlist generation function. Feature_data is the list of tracks and their associated music feature data retrieved from spotify.
    The algorithm will check the users predicted emotion from per_song and this dictionary tells the algorithm how many of each song's emotion type will be added 
    to the final playlist based on the music feature data. The mapping between valence and energy is calculated based on Thayers 2-D Emotional Model 
    http://www.icact.org/upload/2011/0386/20110386_finalpaper.pdf
    """
    playlist_tracks = []  

    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    # all_tracks
    all_tracks = df.copy() 
    all_tracks = all_tracks.drop(['energy', 'valence'], axis=1)
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)       

    # joy_tracks
    joy_tracks = df.copy()
    joy_tracks = joy_tracks[joy_tracks['energy'] > 0.5]
    joy_tracks = joy_tracks[joy_tracks['valence'] > 0.5]
    # shuffle joy_tracks
    joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True)

    # anger_tracks
    anger_tracks = df.copy()
    anger_tracks = anger_tracks[anger_tracks['energy'] > 0.5]
    anger_tracks = anger_tracks[anger_tracks['valence'] < 0.5]
    # shuffle anger_tracks
    anger_tracks = anger_tracks.sample(frac=1).reset_index(drop=True)

    # sad_tracks
    sad_tracks = df.copy()
    sad_tracks = sad_tracks[sad_tracks['energy'] < 0.5]
    sad_tracks = sad_tracks[sad_tracks['valence'] < 0.5]
    # shuffle sad_tracks
    sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
    
    # calm_tracks
    calm_tracks = df.copy()
    calm_tracks = calm_tracks[calm_tracks['energy'] < 0.5]
    calm_tracks = calm_tracks[calm_tracks['valence'] > 0.5]
    # shuffle calm_tracks
    calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)

    # check what tones have been calculated
    tone_scores = [0, 0, 0, 0]
    songs_per_tone = [0, 0, 0, 0]
                # joy[0],anger[1],sadness[2],calm[3]

    # fill tone_scores
    if 'joy' in tones.keys():
        tone_scores[0] = tones['joy']
    if 'anger' in tones.keys():
        tone_scores[1] = tones['anger']
    if 'sadness' in tones.keys():
        tone_scores[2] = tones['sadness']
    if 'calm' in tones.keys():
        tone_scores[3] = tones['calm']

    # fill tone_songs
    if 'joy' in per_song.keys():
        songs_per_tone[0] = per_song['joy']
    if 'anger' in per_song.keys():
        songs_per_tone[1] = per_song['anger']
    if 'sadness' in per_song.keys():
        songs_per_tone[2] = per_song['sadness']
    if 'calm' in per_song.keys():
        songs_per_tone[3] = per_song['calm']

    # loop, only decrementing the counter when a song is added to playlist__tracks list of ids
    count1 = 0
    while(count1 < num_songs):
        for i in range(len(tone_scores)):               # repeatedly loop through each song type
            if songs_per_tone[i] == 0:                  # no songs to add of this emotion
                i += 1                                  # skip to next song type in list
            # Joy
            elif songs_per_tone[i] > 0 and i == 0:      # songs_per_tone[0] = 25    aka: there are 25 joy songs left to be added to the final playlist      
                temp_song = joy_tracks.at[0, 'id']      # joy song to be added to playlist
                if temp_song not in playlist_tracks:    # Prevent duplicate tracks
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1              # Decrement the song_per_tone value since we added a song to the playlist
                    joy_tracks.drop(0)                  # Remove this track from the dataframe since we have added it
                    joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True) # Shuffle the dataframe
                    count1 += 1
                else: 
                    joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True) # Well the track was already in the playlist, so lets shuffle the joy_track list
            # Anger
            elif songs_per_tone[i] > 0 and i == 1:
                temp_song = anger_tracks.at[0, 'id']
                if temp_song not in playlist_tracks:
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                    anger_tracks.drop(0)
                    anger_tracks = anger_tracks.sample(frac=1).reset_index(drop=True)
                    count1 += 1
                else:
                    anger_tracks = anger_tracks.sample(frac=1).reset_index(drop=True)
            # Sad
            elif songs_per_tone[i] > 0 and i == 2:
                temp_song = sad_tracks.at[0, 'id']
                if temp_song not in playlist_tracks:
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                    sad_tracks.drop(0)
                    sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
                    count1 += 1
                else:
                    sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
            # Calm 
            elif songs_per_tone[i] > 0 and i == 3:
                temp_song = calm_tracks.at[0, 'id']
                if temp_song not in playlist_tracks:
                    playlist_tracks.append(temp_song)
                    songs_per_tone[i] -= 1
                    calm_tracks.drop(0)
                    calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)
                    count1 += 1
                else:
                    calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)
            # Empty List
            elif (songs_per_tone[0] == 0) and (songs_per_tone[1] == 0) and (songs_per_tone[2] == 0) and (songs_per_tone[3] == 0):
                temp_song = all_tracks.at[0, 'id']
                if temp_song not in playlist_tracks:
                    playlist_tracks.append(temp_song)
                    # songs_per_tone[i] -= 1
                    all_tracks.drop(0)
                    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
                    count1 += 1
                else:
                    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)

    return playlist_tracks
   

def random_rs(feature_data, num_songs):
    """Given music feature data, it ditches the columns of music feature data and instead generates a random playlist using a list of track ids.
    This is an alternative playlist generation method, and it is currently not in use. """
    playlist_tracks = []
    
    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    # all_tracks
    all_tracks = df.copy() 
    all_tracks = all_tracks.drop(['energy', 'valence'], axis=1)
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
    
    count1 = 0
    while count1 < num_songs:
        temp_song = all_tracks.at[0, 'id']
        if temp_song not in playlist_tracks:
            playlist_tracks.append(temp_song)
            all_tracks.drop(0)
            all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
            count1 += 1
        else: 
            all_tracks = all_tracks.sample(frac=1).reset_index(drop=True) 
    
    return playlist_tracks

def joy_rs(feature_data, num_songs):
    """This is alternate playlist generation function, it creates a playlist of songs which are measured to have certain valence and energy statistics which represent 
    joyful songs. """
    playlist_tracks = []

    # Lets keep the playlist size range between 25-50 
    tot_songs = num_songs
    if tot_songs > 50:
        tot_songs = 50

    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    # all_tracks
    all_tracks = df.copy() 
    all_tracks = all_tracks.drop(['energy', 'valence'], axis=1)
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)

    # joy_tracks
    joy_tracks = df.copy()
    joy_tracks = joy_tracks[joy_tracks['energy'] > 0.5]
    joy_tracks = joy_tracks[joy_tracks['valence'] > 0.5]
    joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True)

    count1 = 0
    while count1 < tot_songs:
        if joy_tracks.size > 0:
            temp_song = joy_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                joy_tracks.drop(0)
                joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else: 
                joy_tracks = joy_tracks.sample(frac=1).reset_index(drop=True)
        else:
            # Pull random tracks from all_tracks
            temp_song = all_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                all_tracks.drop(0)
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else:
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
    
    return playlist_tracks

def anger_rs(feature_data, num_songs):
    """This is alternate playlist generation function, it creates a playlist of songs which are measured to have certain valence and energy statistics which represent 
    angry songs. """
    playlist_tracks = []

    # Lets keep the playlist size range between 25-50 
    tot_songs = num_songs
    if tot_songs > 50:
        tot_songs = 50

    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    # all_tracks
    all_tracks = df.copy()
    all_tracks = all_tracks.drop(['energy', 'valence'], axis=1) 
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)

    # ang_tracks
    ang_tracks = df.copy()
    ang_tracks = ang_tracks[ang_tracks['energy'] > 0.5]
    ang_tracks = ang_tracks[ang_tracks['valence'] < 0.5]
    ang_tracks = ang_tracks.sample(frac=1).reset_index(drop=True)

    count1 = 0
    while count1 < tot_songs:
        if ang_tracks.size > 0:
            temp_song = ang_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                ang_tracks.drop(0)
                ang_tracks = ang_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else: 
                ang_tracks = ang_tracks.sample(frac=1).reset_index(drop=True)
        else:
            # Pull random tracks from all_tracks
            temp_song = all_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                all_tracks.drop(0)
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else:
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
    
    return playlist_tracks

def sad_rs(feature_data, num_songs):
    """This is alternate playlist generation function, it creates a playlist of songs which are measured to have certain valence and energy statistics which represent 
    sad songs. """
    playlist_tracks = []

    # Lets keep the playlist size range between 25-50 
    tot_songs = num_songs
    if tot_songs > 50:
        tot_songs = 50

    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    # all_tracks
    all_tracks = df.copy()
    all_tracks = all_tracks.drop(['energy', 'valence'], axis=1) 
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)

    # sad_tracks
    sad_tracks = df.copy()
    sad_tracks = sad_tracks[sad_tracks['energy'] < 0.5]
    sad_tracks = sad_tracks[sad_tracks['valence'] < 0.5]
    sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)

    count1 = 0
    while count1 < tot_songs:
        if sad_tracks.size > 0:
            temp_song = sad_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                sad_tracks.drop(0)
                sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else: 
                sad_tracks = sad_tracks.sample(frac=1).reset_index(drop=True)
        else:
            # Pull random tracks from all_tracks
            temp_song = all_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                all_tracks.drop(0)
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else:
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
    
    return playlist_tracks

def calm_rs(feature_data, num_songs):
    """This is alternate playlist generation function, it creates a playlist of songs which are measured to have certain valence and energy statistics which represent 
    calm songs. """
    playlist_tracks = []

    # Lets keep the playlist size range between 25-50 
    tot_songs = num_songs
    if tot_songs > 50:
        tot_songs = 50

    # using pandas dataframe to manipulate songs
    df = pd.DataFrame.from_dict(feature_data)

    # all_tracks
    all_tracks = df.copy()
    all_tracks = all_tracks.drop(['energy', 'valence'], axis=1) 
    all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)

    # calm_tracks
    calm_tracks = df.copy()
    calm_tracks = calm_tracks[calm_tracks['energy'] < 0.5]
    calm_tracks = calm_tracks[calm_tracks['valence'] > 0.5]
    calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)

    count1 = 0
    while count1 < tot_songs:
        if calm_tracks.size > 0:
            temp_song = calm_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                calm_tracks.drop(0)
                calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else: 
                calm_tracks = calm_tracks.sample(frac=1).reset_index(drop=True)
        else:
            # Pull random tracks from all_tracks
            temp_song = all_tracks.at[0, 'id']
            if temp_song not in playlist_tracks:
                playlist_tracks.append(temp_song)
                all_tracks.drop(0)
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
                count1 += 1
            else:
                all_tracks = all_tracks.sample(frac=1).reset_index(drop=True)
    
    return playlist_tracks


    
 

