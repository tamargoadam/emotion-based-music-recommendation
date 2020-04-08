import tweepy
import json
import re
# path = 'data/'


def get_twitter_api() -> tweepy.API:
    """authenticates twitter and uses auth info to create and return a tweepy API"""
    with open("../credentials/twitter_credentials.json", "r") as file:
        creds = json.load(file)
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_KEY'], creds['ACCESS_SECRET'])
    return tweepy.API(auth)


def remove_url(txt: str) -> str:
    """remove urls from tweets"""
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def get_tweets_by_user(username: str, num_tweets: int = 1) -> list:
    """get user's 'num_tweets' most recent tweets"""
    api = get_twitter_api()
    tweets_data = api.user_timeline(screen_name=username)
    tweets = [tweet_data.text for tweet_data in tweets_data]
    return tweets[:num_tweets]

#200 is maximum amount of tweets at a time
def get_all_tweets(username: str) -> list:
    api = get_twitter_api() 
    alltweets = api.user_timeline(screen_name = username, count=200)
    outtweets = [remove_url(tweet.text) for tweet in alltweets]
    return outtweets

