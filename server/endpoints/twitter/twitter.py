import tweepy
import json
import csv
import re
path = 'data/'

def get_twitter_api():
    """authenticates twitter and uses auth info to create and return a tweepy API"""
    with open("../credentials/twitter_credentials.json", "r") as file:
        creds = json.load(file)
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_KEY'], creds['ACCESS_SECRET'])
    return tweepy.API(auth)

# Helper function to remove urls from tweets
def remove_url(txt):
    #remove stuff from our tweets we don't want
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


# Helper function to get ALL 3000+ tweets of a specified user
# Source: https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_name):
    api = get_twitter_api() #always need this when making twitter api calls!
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
        ### END OF WHILE LOOP ###
      # transform the tweepy tweets into a 2D array that will populate the csv
      # tweepy status object properties can be found here:
      # https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04
    outtweets = [[remove_url(tweet.text)] for tweet in alltweets]
    # write the csv
    #save_json('%s_tweets.csv' % screen_name, outtweets)
    with open(path + '%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["text"])
        writer.writerows(outtweets)
    pass



#get_all_tweets('timdoozy')  # --> data/timdoozy_tweets.csv
#get_all_tweets('billsimmons')   # --> data/billsimmons_tweets.csv
#get_all_tweets('tamargoadam')   # --> data/tamargoadam_tweets.csv
get_all_tweets('timdoozy')