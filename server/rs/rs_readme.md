# Music Recommendation System Files

## RS.py
##### get_sentiment(user_name):
    Input: (twitter_screen_name)
    Output: (sentiment scores for a user)
    What it does: Given a specific user as input, it gets that user's sentiment.
    
##### get_music_pref_features(user_name):
    Input: (twitter_screen_name)
    Output: (audio features for several tracks)
    What it does: For a user, we will get audio analysis for several song tracks.

    What song tracks? We will consider consider 50 songs from a user's music preferences, and we will consider 50 songs that is similar to the user's music preferences. 

##### analyze_music_features(user_name):
    Input: (twitter_screen_name)
    Output: (aggregate music feature scores)
    What it does: For a user, we will analyze the mean values of the music features. Valence, speechiness, liveness, instrumentalness, energy, danceability and acousticness. 
    
##### compare_data():
    compares sentiment and music feature data

##### General purpose tones given:
    Anger, Fear, Joy, Sadness, Analytical, Confident, Tentative

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
