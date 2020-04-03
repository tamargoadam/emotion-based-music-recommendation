import os
import tweepy
import re
# path = 'data/'


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


"""
def get_all_tweets(screen_name):
    # Helper function to get ALL 3000+ tweets of a specified user
    # Source: https://gist.github.com/yanofsky/5436496
    api = get_twitter_api() # always need this when making twitter api calls!
    alltweets = []
    # (200 is the maximum allowed count at a time)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one to avoid duplication
    oldest = alltweets[-1].id - 1
    # keep grabbing tweets until there are no tweets left
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        # all subsequent requests use the max_id param to prevent
        # duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
        # END OF WHILE LOOP
    # transform the tweepy tweets into a 2D array that will populate the csv
    # tweepy status object properties can be found here:
    # https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04
    outtweets = [[remove_url(tweet.text)] for tweet in alltweets]
    # write the csv
    # save_json('%s_tweets.csv' % screen_name, outtweets)
    with open(path + '%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["text"])
        writer.writerows(outtweets)
    pass
"""
