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
    """Helper function for get_tweets() used to remove any urls or special symbols found in tweets."""
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def get_tweets(screen_name: str) -> list:
    """Retrieves a list of the most recent 200 tweets for a given user. Links will be removed from tweets.
    Returns an empty list if there are no tweets found for the given user."""
    api = get_twitter_api() 
    try:
        alltweets = api.user_timeline(screen_name=screen_name, count=200)
        outtweets = [remove_url(tweet.text) for tweet in alltweets]
        if len(outtweets) == 0:
            raise NoTweetsFound
        return outtweets
    except NoTweetsFound:
        print(f'No tweets were found for the twitter account of {screen_name}.')


class NoTweetsFound(Exception):
    pass