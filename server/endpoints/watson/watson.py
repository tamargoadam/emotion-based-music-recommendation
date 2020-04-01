import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_tone_analyzer():
    with open("../credentials/watson_credentials.json", "r") as file:
        creds = json.load(file)
        authenticator = IAMAuthenticator(creds['API_KEY'])
        tone_analyzer = ToneAnalyzerV3(
            version=creds['VERSION'],
            authenticator=authenticator)
        tone_analyzer.set_service_url(creds['URL'])
    return tone_analyzer


# 
def get_sentiment(tweets: list):
    # tone analyzer api call from sentiment.json data
    tones = []
    for tweet in tweets:
        tones.append(get_tone_analyzer().tone(
            tone_input=tweet,
            content_type='text/plain',
            sentences=True).get_result())
    print(tones)
    


