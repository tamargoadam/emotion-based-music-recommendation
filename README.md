# Emotion-Based Music Recommendation Docs

## Getting Started Guide
In order to use this service, you *must have __both__* the Backend and the Frontend server running. Additionally you will need to have set the environment variables in sample.env and rename the file to .env

### To Start the Backend Server
Flask is used as the backend server to serve particular routes for handling API requests. 
```
pipenv install
pipenv shell
python server/api/routes.py
```

### To Start the Frontend Server
Preact is utilized as the JavaScript framework to render client side HTML. Preact is a lightweight alternative to React.
```
cd client
npm install
npm run dev
```

### Connect with API's and set the environment variables
You will need to fill out the sample sample.env file with your own environment variables. In order to gain access to these variables you will have to setup a Spotify, Twitter and IBM-Watson developer account. 
[Access the Twitter Developer Dashboard](https://developer.twitter.com/)
[Create a new app on the Spotify Developer Dashboard](https://developer.spotify.com/)
[Create an IBM-Watson Developer Account](https://cloud.ibm.com/registration?target=%2Fapidocs%2Ftone-analyzer)

### Read the API documentations
[Learn how to use Spotipy](https://spotipy.readthedocs.io/)
[Learn how to use Tweepy](http://docs.tweepy.org/en/latest/)
[Learn more about IBM-Watson's Tone Analyzer](https://cloud.ibm.com/apidocs/tone-analyzer)




