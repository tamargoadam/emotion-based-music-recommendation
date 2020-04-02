# import json
from endpoints.watson import watson
from endpoints.twitter import twitter


def get_sentiment(screen_name: str, num_tweets: int = 1) -> list:
    """generate list of sentiments corresponding to user's tweets"""
    sentiment_data = watson.get_sentiment(twitter.get_tweets_by_user(screen_name, num_tweets))
    # TODO: fix credential path issue

    tones = []
    for t in sentiment_data['document_tone']['tones']:
        tone_score = dict(tone=t['tone_name'], score=t['score'])
        print(tone_score)
        tones.append(tone_score)
    return tones


def normalize_data(name):    
    """
    # normalize data from spotify that isnt from 0-1
    # also consider normalizing data from watson from 0-1

    from sklearn import preprocessing
    loudness = songs[['loudness']].values
    min_max_scaler = preprocessing.MinMaxScaler()
    loudness_scaled = min_max_scaler.fit_transform(loudness)
    """


def cluster_songs(name):
    """
    # cluster the songs and identify moods represented by each cluster
    # use k-means clustering algorithm, good at finding distributions in data
    
    # challenge!! finding optimal number k
    # Elbow method: run k-means for a range of k
    # plot the average sum of squares distance to cluster center vs the number of clusters
    # visual elbow = optimal number of clusters

    from sklearn.cluster import KMeans
    Sum_of_squared_distances = []
    K = range(1,15)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(songs_features)
        Sum_of_squared_distances.append(km.inertia_)
    """


def cluster_moods(name):
    """
    # identify the moods associated with each cluster from the user data
    #

    """


get_sentiment('atamargo')
