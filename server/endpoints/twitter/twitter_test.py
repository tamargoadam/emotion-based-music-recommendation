import tweepy
import json
import csv
import pandas as pd
import datetime


def get_twitter_api():
    """authenticates twitter and uses auth info to create and return a tweepy API"""
    with open("../credentials/twitter_credentials.json", "r") as file:
        creds = json.load(file)
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_KEY'], creds['ACCESS_SECRET'])
    return tweepy.API(auth)

def get_tweets_by_user(username: str, num_tweets: int = 20):
    """get user's 'num_tweets' most recent tweets"""
    api = get_twitter_api()
    tweets_data = api.user_timeline(screen_name=username)
    tweets = [tweet_data.text for tweet_data in tweets_data]
    return tweets[:num_tweets]
    #returns a list of status objects ['tweet1 text', 'tweet2 text', ..]

print(get_tweets_by_user('timdoozy'))

#run this method if it is a NEW user
def get_all_tweets(screen_name):
    # auth twitter
    api = get_twitter_api()
    
    #empty list of tweets
    alltweets = []
    #get 200 most recent tweets from timeline
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)
    #add new tweets
    alltweets.extend(new_tweets)
    # save id of oldest tweet minus 1
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are none left
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
    #transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
    #write the csv	
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass

if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("timdoozy")
