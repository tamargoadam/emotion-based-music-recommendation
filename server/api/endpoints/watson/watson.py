import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#from endpoints.twitter.twitter import *

def get_tone_analyzer() -> ToneAnalyzerV3:
    authenticator = IAMAuthenticator(os.environ['WATSON_API_KEY'])
    tone_analyzer = ToneAnalyzerV3(
        version=os.environ['WATSON_VERSION'],
        authenticator=authenticator)
    tone_analyzer.set_service_url(os.environ['WATSON_URL'])
    return tone_analyzer

""" # Used for testing
def get_tone_analyzer() -> ToneAnalyzerV3:
    with open("watson_credentials.json", "r") as file:
        creds = json.load(file)
        authenticator = IAMAuthenticator(creds['API_KEY'])
        tone_analyzer = ToneAnalyzerV3(
            version=creds['VERSION'],
            authenticator=authenticator)
        tone_analyzer.set_service_url(creds['URL'])
    return tone_analyzer
"""

def get_sentiment(tweets: list) -> list:
    """tone analyzer api call from sentiment.json data"""
    tweet_str = tweets_to_string(tweets) 
    ret = get_tone_analyzer().tone(
            tone_input=tweet_str,
            content_type='text/plain',
            sentences=True).get_result()
    #ret = format_sentiment(ret) #function to clean output of get_sentiment(), make call separately
    return ret

def sort_tones(d1: dict) -> dict:
    #organizes output of tones to 4 tone categories (joy, sadness, anger, calm)
    output = {}
    temp_calm = 0
    temp_fear = 0
    temp_sad = 0
    temp_joy = 0
    temp_anger = 0
    
    counter = 0
    
    for i in d1:
        if i == 'confident' or i == 'tentative' or i == 'analytical':
            temp_calm += d1.get(i)
            counter += 1
        if i == 'fear':
            temp_fear += d1.get(i)
        if i == 'joy':
            temp_joy += d1.get(i)
        if i == 'sadness':
            temp_sad += d1.get(i)
        if i == 'anger':
            temp_anger += d1.get(i)
    #end of for loop
    
    #check if fear was measured
    if temp_fear > 0 and temp_calm > 0:
        if temp_calm - temp_fear > 0:
            temp_calm = temp_calm - temp_fear
            
    #check if calm was measured
    #find average of multiple calm tones
    if temp_calm > 0 and counter > 0:
        temp_calm = temp_calm / counter
    
    #double check calm score is > 0
    if temp_calm > 0:
        output.update( {'calm': temp_calm })
    #end of calm
    
    if temp_sad > 0:
        output.update( {'sadness': temp_sad} )
    if temp_joy > 0:
        output.update( {'joy': temp_joy} )
    if temp_anger > 0:
        output.update( {'anger': temp_anger} )
    
    return output


def format_sentiment(xd):
    #clean up output of get_sentiment
    #output is a dictionary of the returned document tones
    tone_out = xd
    tone_out = tone_out.get('document_tone')
    tone_out = tone_out.get('tones')

    output = {}
    length = len(tone_out)
    i = 0
    x_1 = [] #scores
    x_2 = [] #names

    while(i < length):
        temp = tone_out[i]
        for key in temp:
            if key == 'score':
                x_1.append(temp.get(key))
            if key == 'tone_id':
                x_2.append(temp.get(key))
        i = i + 1
    #end of while loop
    
    length = len(x_1) 
    for i in range(length): 
        output.update( { x_2[i] : x_1[i] } )
    #end of for loop
    
    return output

def tweets_to_string(tweets: list):
    #converts a list of tweets to a single string without "RT "s and periods in between tweets.
    ret = ""
    for i in tweets: 
        rts = i[0]
        rts += i[1]
        rts += i[2]
        if(rts == "RT "):
            x = len(i)
            i = i[3:x]
        ret += i
        ret += ". "
    return ret

#TESTING WATSON METHODS
#tweet_test = twitter.get_all_tweets('timdoozy')
#tones = get_sentiment(tweet_test)
#tones = format_sentiment(tones)
#print(tones)

#EXPECTED OUTPUT:
#{'joy': 0.617, 'anger': 0.542}