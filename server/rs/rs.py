import json

wpath = '../watson/data/'

# Function to read the watson sentiment data 
def get_sentiment(screen_name):
    # open user .json data found at: `watson/data/%s_sentiment.json`
    f = open(wpath + '%s_sentiment.json' % screen_name,)
    data = json.load(f)

    tones = []
    for i in data['document_tone']['tones']:
        thisdict = dict(tone=i['tone_name'], score=i['score'])
        print(thisdict)
        tones.append(thisdict)
    # save the document tones as a new json file
    with open('data/' + '%s_data.json' % screen_name, 'w', encoding='utf-8') as outfile:
        json.dump(tones, outfile, ensure_ascii=False, indent=2)
    f.close()
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


get_sentiment('timdoozy')