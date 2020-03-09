import tweepy
import json


def get_twitter_api():
    """authenticates twitter and uses auth info to create and return a tweepy API"""
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)
    auth = tweepy.OAuthHandler(creds['CUSTOMER_KEY'], creds['CUSTOMER_SECRET'])
    auth.set_access_token(creds['ACCESS_KEY'], creds['ACCESS_SECRET'])
    return tweepy.API(auth)


def get_tweets_by_user(username: str, num_tweets: int = 1):
    """get user's 'num_tweets' most recent tweets"""
    api = get_twitter_api()
    tweets_data = api.user_timeline(screen_name=username)
    tweets = [tweet_data.text for tweet_data in tweets_data]
    return tweets[:num_tweets-1]

