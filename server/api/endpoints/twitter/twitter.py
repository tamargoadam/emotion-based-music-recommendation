import os
import tweepy
import re


def get_twitter_api() -> tweepy.API:
    """authenticates twitter and uses auth info to create and return a tweepy API"""
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
    return tweepy.API(auth)


def validate_user_exists(username: str) -> bool:
    api = get_twitter_api()
    try:
        api.get_user(username)
    except Exception:
        return False
    return True


def remove_url(txt: str) -> str:
    """remove urls from tweets"""
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def get_tweets_by_user(username: str, num_tweets: int = 1) -> list:
    """get user's 'num_tweets' most recent tweets"""
    api = get_twitter_api()
    tweets_data = api.user_timeline(screen_name=username)
    tweets = [tweet_data.text for tweet_data in tweets_data]
    return tweets[:num_tweets]


# 200 is maximum amount of tweets at a time
def get_all_tweets(username: str) -> list:
    api = get_twitter_api() 
    alltweets = api.user_timeline(screen_name = username, count=200)
    outtweets = [remove_url(tweet.text) for tweet in alltweets]
    return outtweets

