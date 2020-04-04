from endpoints.watson import watson
from endpoints.twitter import twitter
from endpoints.spotify import spotify
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.multiclass import unique_labels
import pandas as pd
import random
from __future__ import division, print_function, unicode_literals
import os
# Ignore useless warnings (see SciPy issue #5998)
import warnings
warnings.filterwarnings(action="ignore", message="^internal gelsd")

np.random.seed()    #use a random seed

import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

from sklearn.metrics import silhouette_score


def get_sentiment(username: str) -> list:
    """generate list of sentiments corresponding to user's tweets"""
    sentiment_data = watson.get_sentiment(twitter.get_tweets_by_user(username))
    # TODO: fix credential path issue

    tones = []
    for t in sentiment_data['document_tone']['tones']:
        tone_score = dict(tone=t['tone_name'], score=t['score'])
        print(tone_score)
        tones.append(tone_score)
    return tones

def get_spotify_playlist_data(username: str) -> list:
    scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'
    redirect_uri = 'https://localhost:8000/callback'
    token = spotify.get_user_token(username, scope, redirect_uri)
    if token:
        print('Success, got spotify token')
    else:
        print("Cant get token for ", username)
    sp = spotify.authenticate_spotify(token)
    trackList = spotify.get_all_songs(username, sp)
    trackList = spotify.get_tracks_with_features(trackList, sp)
    return trackList

def check_key(dict, key) -> bool:
    if key in dict.keys():
        return True
    else
        return False

def sentiment_recommendation(username: str) -> list: 
    tones = get_sentiment(username)
    music = get_spotify_playlist_data(username)
    #songs = pd.DataFrame.from_dict(trackList)
    tones = pd.DataFrame.from_dict(tones)
    #tones: anger, fear, joy, sadness, analytical, confident, tentative
    anger, fear, joy, sadness, analytical, confident, tentative = 0 
    if check_key(tones, 'anger'):
        anger = True 
    if check_key(tones, 'fear'):
        fear = True 
    if check_key(tones, 'joy'):
        joy = True
    if check_key(tones, 'sadness'):
        sadness = True 
    if check_key(tones, 'analytical'):
        analytical = True 
    if check_key(tones, 'confident'):
        confident = True 
    if check_key(tones, 'tentative'):
        tentative = True 
## Machine Learning Functions Below -- not entirely functional yet
def normalize_data(username: str) -> list:
    #preprocessing
    songs = get_spotify_playlist_data(username)
    songs = pd.read_dict()  #set the dataframe
    #scale loudness
    loudness = songs[['loudness']].values
    min_max_scaler = preprocessing.MinMaxScaler()
    loudness_scaled = min_max_scaler.fit_transform(loudness)
    songs['loudness'] = pd.DataFrame(loudness_scaled)
    #scale tempo
    tempo = songs[['tempo']].values
    min_max_scaler = preprocessing.MinMaxScaler()
    tempo_scaled = min_max_scaler.fit_transform(loudness)
    songs['tempo'] = pd.DataFrame(tempo_scaled)
    #dont drop any data yet
    return song_features 

    # remove song names, artist and id before clustering
    #song_features = songs.copy()
    #song_features = song_features.drop(['id'],axis=1)
    #songs_features = songs_features.drop(['name','artist','id'],axis=1)    #name and artist should not be within the data, i removed it
    #return song_features 

def ml_rec_alg(username: str) -> list: 
    trackList = normalize_data(username) #gets all tracks and normalizes the data 
    np.random.seed()
    songs = pd.DataFrame.from_dict(trackList)
    #songs.info()   #dictionary info
    #songs.head()   #head of dict

    #drop data not needed 
    songs_features = songs.copy()
    songs_features = songs_features.drop(['id','instrumentalness','acousticness','name','artist','liveness'],axis=1)

    #find optimal k value   --not using yet
    #op_k = find_optimal_k_value(songs_features)
    #its probably going to be between 2-4, for now assume its 4 for the 4 basic emotions
    op_k = 4
    kmeans = KMeans(n_clusters=op_k)
    kmeans.fit(songs_features)
    #reduce data to 2 dimensions
    y_kmeans = kmeans.predict(songs_features)
    #pca = PCA(n_components=2)
    #principal_components = pca.fit_transform(songs_features)
    #pc = pd.DataFrame(principal_components)
    X = songs_features
    y = y_kmeans
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    rfc = RandomForestClassifier(n_estimators=100,criterion='gini')
    rfc.fit(X_train,y_train)
    # Predicting the Test set results
    y_pred = rfc.predict(X_test)

def find_optimal_k_value(songlist: list) -> int:
    #given an input of data, return the best guess for an optimal K value
    Sum_of_squared_distances = []
    K = range(1,15)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(songs_features)
        Sum_of_squared_distances.append(km.inertia_)
    
    for n_clusters in range(2,15):
        clusterer = KMeans (n_clusters=n_clusters)
        preds = clusterer.fit_predict(songs_features)
        centers = clusterer.cluster_centers_

    score = silhouette_score (songs_features, preds, metric='euclidean')
    print ("For n_clusters = {}, silhouette score is {})".format(n_clusters, score))


