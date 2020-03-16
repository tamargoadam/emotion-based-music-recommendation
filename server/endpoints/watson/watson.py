import json
import os
from os.path import join
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import pandas as pd 
from datetime import date
from datetime import datetime
import time

import preprocessor as p

import re
from textblob import TextBlob

wpath = 'data/'
tpath = '../twitter/data/'

#Authentication Method
with open("../credentials/watson_credentials.json", "r") as file:
        creds = json.load(file)
        authenticator = IAMAuthenticator(creds['API_KEY'])
        tone_analyzer = ToneAnalyzerV3(
        version=creds['VERSION'],
        authenticator=authenticator)
        tone_analyzer.set_service_url(creds['URL'])

#Start of Methods
def get_sentiment(screen_name):
    # Input: '../twitter_data/%s_tweets.csv'
    #data = pd.read_csv(tpath + '%s_tweets.csv' % screen_name, usecols=['text'], decimal=",", index_col=False, nrows=50)
    #print(data)
    #json_text_data = ""
    #for index, sentiment in data['text'].iteritems():
        #json_text_data = json_text_data + sentiment + ". "
        #output = tone_analyzer.tone(sentiment, content_type='text/plain')
    #print(json_text_data)
    #x = { "text" : json_text_data }
    #y = json.dumps(x)
    #with open(wpath + '%s_sentiment.json' % screen_name, 'w') as outfile:
        #json.dump(y, outfile)

    
    with open(join(os.getcwd(), 'data/test.json')) as tone_json:
        tone = tone_analyzer.tone(
            tone_input=json.load(tone_json)['text'],
            content_type='text/plain',
            sentences=True).get_result()

    print(json.dumps(tone, indent=2))

    #data.to_csv(wpath + '%s_sentiment.csv')


get_sentiment('timdoozy')