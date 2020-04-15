# Music Recommendation System Files

## RS.py
## Following the Flow:
##### playlist_rs(feature_data, tones, per_song, num_song)
    Returns a list of track ids to be used to create a playlist from the recommendation algorithm
    
##### rs(twitter_name, spotify_name, num_songs) 
    Performs sentiment analysis of user's most recent 200 tweets.
    Collects spotify tracks saved in library, playlists, and the top tracks from favorite artists and similar artists.
    Identifies user emotion and weighs the amount of songs per emotion to populate the playlist with.
    Fills a playlist with music recommendations predicting a users preferences based on their predicted emotions.

    Predict if a user is: Joyful, Angry, Sad, Calm.
    Based on these predictions recommend songs that are of these emotions based on the collected songs valence and energy. 

##### get_tones(user_name):
    Input: twitter_name
    Output: dictionary of document tones analyzed by watson

##### adjust_songs(dict, int):
    Input: a dictionary of the tone scores retrieved from get_tones()
    Input2: the number of songs requested to be in the final playlist
    Output: the number of songs per tone score to populate in the final playlist.

##### show_vals(int, int, int, int): helper function
    Inputs: [sad, joy, anger, calm]
    Output: printing each score to screen

##### General purpose tones given:
    Anger, Fear, Joy, Sadness, Analytical, Confident, Tentative
    Confidence scores from 0-1.

##### General music features given:
    Acousticness: (0-1 confidence measure), 1 represents high confidence the track is acoustic.

    Danceability: (0-1) how suitable the track is for dancing based on tempo, rhythm, stability, beat strength, and overall regularity. 1 is most dancable. 0 least.

    Energy: (0-1) measure of intensity and activity. An energetic track is fast, loud and noisy. Death metal is high energy, Bach is not.

    Instrumentalness: (0-1) does the track contain vocals. values above 0.5 are intended to represent instrumental tracks. Confidence is higher as value approaches 1.

    Loudness: (-60-0 db) loudness of track in decibels (dB). Values are averaged across the entire track and are useful for comparing the relative loudness of tracks. Its the quality of sound that is the primary psychological correlate of physical strength (amplitude). 

    Speechiness: (0-1) presence of spoken words in a track. Talk shows, audiobooks and poetry is very close to 1. Values above 0.66 are tracks entirely spoken of words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, rap music. Values below 0.33 are music tracks.

    Valence: (0-1) musical positiveness of a track. High valence = happy, cheerful, euphoric. Low valence = sad, depressed, angry.

    Tempo: Estimated overall tempo of a track in beats per minute (BPM). Tempo is the pace. Ever see the movie Whiplash? "Not quite my tempo."

    Arousal (degree of calmness or stimulation evoked by music)

##### 
