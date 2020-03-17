import json
import os
from os.path import join
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pandas as pd 

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


# 
def get_sentiment(screen_name):
    # Input: '../twitter/data/%s_tweets.csv'
    # Output: '../watson/data/%s_sentiment.json'
    data = pd.read_csv(tpath + '%s_tweets.csv' % screen_name, usecols=['text'], decimal=",", index_col=False, nrows=50)
    json_text_data = ""
    for index, sentiment in data['text'].iteritems():
        json_text_data = json_text_data + sentiment + ". "
    print(json_text_data)
    with open(wpath + '%s_sentiment.json' % screen_name, 'w') as f:
        json.dump(json_text_data, f)

    x = { "text" : json_text_data }
    with open(wpath + '%s_sentiment.json' % screen_name, 'w') as outfile:
        json.dump(x, outfile)


    # tone analyzer api call from sentiment.json data
    with open(join(os.getcwd(), wpath + '%s_sentiment.json' % screen_name)) as tone_json:
        tone = tone_analyzer.tone(
            tone_input=json.load(tone_json)['text'],
            content_type='text/plain',
            sentences=True).get_result()
    #print(json.dumps(tone, indent=2))


    # save results as sentiment data file for user
    hello = json.dumps(tone)
    output = json.loads(hello)
    with open(wpath + '%s_sentiment.json' % screen_name, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


    #data.to_csv(wpath + '%s_sentiment.csv')
    

get_sentiment('timdoozy')
get_sentiment('billsimmons')
get_sentiment('tamargoadam')