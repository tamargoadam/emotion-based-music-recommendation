import os
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from endpoints.twitter.twitter import *


def get_tone_analyzer() -> ToneAnalyzerV3:
    authenticator = IAMAuthenticator(os.environ['WATSON_API_KEY'])
    tone_analyzer = ToneAnalyzerV3(
        version=os.environ['WATSON_VERSION'],
        authenticator=authenticator)
    tone_analyzer.set_service_url(os.environ['WATSON_URL'])
    return tone_analyzer


# 
def get_sentiment(tweets: list) -> list:
    """tone analyzer api call from sentiment.json data"""
    tones = []
    for tweet in tweets:
        tones.append(get_tone_analyzer().tone(
            tone_input=tweet,
            content_type='text/plain',
            sentences=True).get_result())
    return tones


# print(get_sentiment(get_tweets_by_user('tamargoadam')))
