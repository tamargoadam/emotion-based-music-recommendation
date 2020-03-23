# Testing the endpoints
Clone and enter project repo
```
git clone https://github.com/tamargoadam/emotion-based-music-recommendation.git
cd emotion-based-music-recommendation
```
install dependency manager and dependencies 
(pipenv allows us to manage dependencies)
```
pip install --user pipenv
pipenv install
```
pipenv should've installed the necessary libraries (pandas, tweepy, etc...). now use pipenv to create a virtualenv and run a script.
```
pipenv shell
python3 twitter_popularsearch.py
```

## Temporary
Extract the credential files
```
unzip credentials.zip
```

## Testing Tweets to CSV
Ensure you have dependencies installed before running!
#### IMPORTANT: create a "data" folder within twitter
#### Without the data folder it won't run
from the working directory
```
cd server/endpoints/twitter
```
get user's tweets and save as a .csv file for later
##### get_all_tweets('twitter_username')
```
python3 twitter.py
```
Data is stored @ server/endpoints/twitter/data/%s_tweets.csv
##### NOTE: We can alter the amount of tweets we download, but for testing purposes we have no limit set until we determine one.

## Testing Tweets to Sentiment Data (JSON)
Ensure you have dependencies installed before running!

from the working directory
```
cd server/endpoints/watson
```
get user's tweets as input, send to watson api, save results as json file for later.
##### get_sentiment('twitter_username')
```
python3 watson.py
```
Data is stored @ server/endpoints/watson/data/%s_sentiment.json
##### NOTE: It is imperative that we send a collection of tweets to Watson to reduce the amount of monthly API calls.
