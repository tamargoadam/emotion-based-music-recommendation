import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_watson_api() -> ToneAnalyzerV3:
    """Retrieves a ToneAnalyzerV3 API object, this object is utilized for analyzing the sentiment of Tweets."""
    authenticator = IAMAuthenticator(os.environ['WATSON_API_KEY'])
    tone_analyzer = ToneAnalyzerV3(
        version=os.environ['WATSON_VERSION'],
        authenticator=authenticator)
    tone_analyzer.set_service_url(os.environ['WATSON_URL'])
    return tone_analyzer


def get_tones(tweets: list) -> list:
    """Given a list of tweets as input, get_tones() will convert the list of Tweets into a single string by using the tweets_to_string() helper method,
    then the function will use the Watson API to retrieve a sentiment analysis of the inputted tweets."""
    tweet_str = tweets_to_string(tweets) 
    ret = get_watson_api().tone(
            tone_input=tweet_str,
            content_type='text/plain',
            sentences=True).get_result()
    if ret:
        return ret
    else:
        print('Error in watson.get_tones(). No sentiment data was retrieved by watson.')
        return None


def tweets_to_string(tweets: list):
    """Helper function for get_tones().
    tweets_to_string() converts a list of tweets into a single string
    without "RT "s and periods inbetween tweets."""
    output = ""
    for tweet in tweets: 
        rts = tweet[0:2]
        if rts == "RT ":
            x = len(tweet)
            tweet = tweet[3:x]
        output += tweet
        output += ". "
    return output


def format_tones(tones):
    """This function is used to clean up the output from the get_tones() function. After calling get_tones(), this function
    should be used on that data to narrow its contents. In order to reduce the amount of API calls and to increase the efficiency 
    of this system, all of the user's tweets are analyzed as a document. This means that only one API call is made to IBM Watson's 
    Tone Analyzer. Because of this, a very large dictionary is returned. The formart_tones() function will be used to only extract
    the overall document's tones. This reduces the amount of data being processed at a time."""
    data = tones.get('document_tone')
    data = data.get('tones')

    output = {}
    length = len(data)
    i = 0
    scores = []
    names = [] 

    while i < length:
        temp = data[i]
        for key in temp:
            if key == 'score':
                scores.append(temp.get(key))
            if key == 'tone_id':
                names.append(temp.get(key))
        i = i + 1
    
    for i in range(len(scores)): 
        output.update( { names[i] : scores[i] } )
    
    return output


def sort_tones(tones: dict) -> dict:
    """
    After retrieving the tones from tweets, this function is used in order to sort the dictionary of document tones.
    This function will condense the previous dictionary. It will check to see which tones were found from the users tweets.
    In order to follow the Thayer's emotional mapping model, it will consider the combination of 'confident', 'tentative', 'analytical'
    and 'fear' scores in order to determine the 'calm' emotion. This is done because the Watson API does not give a direct calculation 
    of 'calm' sentiment. This accuracy of this function could be improved!
    """
    output = {}
    confident, tentative, analytical, calm, fear, joy, sadness, anger = 0, 0, 0, 0, 0, 0, 0, 0
    
    for emotion in tones:
        if emotion == 'confident':
            confident += tones.get(emotion)
            counter += 1
        elif emotion == 'tentative':
            tentative += tones.get(emotion)
            counter += 1
        elif emotion == 'analytical':
            analytical += tones.get(emotion)
            counter += 1
        elif emotion == 'fear':
            fear += tones.get(emotion)
        elif emotion == 'joy':
            joy += tones.get(emotion)
        elif emotion == 'sadness':
            sadness += tones.get(emotion)
        elif emotion == 'anger':
            anger += tones.get(emotion)
    
    # if someone is confident and analytical, then they are calm. 
    if confident > 0 and analytical > 0:
        temp = confident + analytical
        calm = temp / 2
    elif confident > 0:
        calm += confident
    elif analytical > 0:
        calm += analytical
    
    # if someone has already been measured as calm, then we will account for fear.
    if calm > 0:
        if fear > 0:
            fear /= 2
            if calm > fear:
                calm -= fear

    # if someone has already been measured as calm, then we will account for tentative.
    if calm > 0:
        if tentative > 0:
            tentative /= 2
            if calm > tentative:
                calm -= tentative

    # if calm is still unchanged, then check for fear and tentative measurements and scale the calm score.
    if calm == 0:
        if fear > 0 and tentative > 0:
            temp = fear + tentative
            calm = temp / 2
        elif fear > 0:
            calm += fear
            calm /= 2
        elif tentative > 0:
            calm += tentative
            calm /= 2

    # Check for each score if its > 0 then we add it to the output dict
    if calm > 0:
        output.update( {'calm': calm })
    if sadness > 0:
        output.update( {'sadness': sadness} )
    if joy > 0:
        output.update( {'joy': joy} )
    if anger > 0:
        output.update( {'anger': anger} )
    
    return output

