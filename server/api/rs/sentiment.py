"""
Sentiment.py

In this file, we will be creating the necessary functions to perform sentiment analysis and to collect 
and store this sentiment data for later analysis and comprehension.
"""
from endpoints.twitter import twitter
from endpoints.watson import watson
import math

def get_sentiment(screen_name):
    """In this function, it will require a Twitter screen_name as input and will return a python dictionary of the calculated sentiment tones from watson.
    This function will return an empty dictionary if no tweets are found
    """
    data = twitter.get_tweets(screen_name)  # data is a list of user tweets
    if data is None:
        return None

    data = watson.get_tones(data)   # data is the tone analysis data provided by watson tone analyzer
    if data is None:
        return None
    
    data = watson.format_tones(data)    # data is a dictionary of the document tones
    if data is None:
        return None

    data = watson.sort_tones(data)  # data is sorted into the main 4 categories of emotion as dictionary
    if data is None:
        return None
    
    return data


def adjust_songs(sentiment: dict, num_songs: int) -> dict:
    """ The adjust_songs() function takes the result from get_sentiment() as well as a number of songs, and it will output
    a dictionary that scales the amount of songs to put in the final playlist for each type of emotion the user has felt."""
    # Returns a new dictionary containing the amount of songs of each tone to produce in the playlist
    calm, joy, anger, sad = 0, 0, 0, 0

    # Loop through dictionary and find tones, count how many tones are found
    count = 0 
    if 'joy' in sentiment.keys():   
        joy = sentiment['joy'] 
        count = count + 1         
    if 'anger' in sentiment.keys():
        anger = sentiment['anger']
        count = count + 1
    if 'sadness' in sentiment.keys():
        sad = sentiment['sadness']
        count = count + 1
    if 'calm' in sentiment.keys():
        calm = sentiment['calm']
        count = count + 1

    # If there are multiple tones, find the reciprocal of count for future calculations
    div = 0
    if count > 0:           
        div = 1 / count
    else: 
        div = 1

    # the position of emotions in the list is predetermined [joy, anger, sad, calm]!
    emotions = [0, 0, 0, 0]
    songs_added = 0

    # for each emotion found in the sentiment dictionary, scale the return amount of songs based on its score.
    if joy > 0:                    
        joy *= num_songs            
        joy *= div                 
        joy = math.floor(joy) 
        emotions[0] = joy         
        songs_added += joy                
    if anger > 0:
        anger *= num_songs
        anger *= div
        anger = math.floor(anger)
        emotions[1] = anger
        songs_added += anger
    if sad > 0:
        sad *= num_songs
        sad *= div
        sad = math.floor(sad)
        emotions[2] = sad
        songs_added += sad
    if calm > 0:
        calm *= num_songs
        calm *= div
        calm = math.floor(calm)
        emotions[3] = calm
        songs_added += calm
        
    # allocate more songs to fill the lists elements to sum equal to the num_songs required in the playlist
    if songs_added < num_songs:                      
        while songs_added < num_songs:              
            for i in range(len(emotions)):
                if emotions[i] == 0:       
                    i += 1                  
                else:
                    emotions[i] = emotions[i] + 1     
                    songs_added += 1
    # deallocate
    elif songs_added > num_songs: 
        while songs_added > num_songs:
            for i in range(len(emotions)):
                if emotions[i] == 0:
                    i += 1
                elif emotions[i] > 1:
                    emotions[i] = emotions[i] - 1 
                    songs_added -= 1
     
    output = sentiment.copy()
    
    # update the output dictionary with new values
    if 'joy' in output.keys():
        output['joy'] = emotions[0]
    if 'anger' in output.keys():
        output['anger'] = emotions[1]
    if 'sadness' in output.keys():
        output['sadness'] = emotions[2]
    if 'calm' in output.keys():
        output['calm'] = emotions[3]
        
    return output
