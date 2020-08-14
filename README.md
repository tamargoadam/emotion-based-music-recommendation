# Emotion-Based Music Recommendation Docs

## Getting Started - Clone and Setup
- Have Python3 and NodeJS installed.
- Acquire developer access keys to the following APIs: [Twitter][twitdev], [Spotify][spotdev], & [IBM-Watson][ibmdev]
-Clone the repository into a new folder called 'ebmr', then move into the 'ebmr' folder and open the directory in your preferred editor
```
git clone https://github.com/tamargoadam/emotion-based-music-recommendation ebmr
cd ebmr
code
```
- Change the environment variables in 'sample.env'  and rename the file to '.env'
- Install pipenv and then use pipenv to install the requirements for this project. 
```
pip install pipenv
pipenv install
```
- Move into the client server directory and then install the front-end dependencies.
```
cd client
npm install
```

## Running the Server
- Within a terminal window, navigate to the project's root directory, 'ebmr'.
- __Start the backend Flask server from within pipenv's shell virtual environment.__
```
pipenv shell
python server/api/routes.py
```
- Open __a new__ terminal window, and navigate to the project's root directory.
- Move into the client folder, and then run the front end server in development mode
```
npm run dev
```

- At this point, you will now be able to access the service and create playlists from [localhost:8080/][localhost]

## Check your Pipfile
- Within Pipfile, alter the python version to match yours. 
```
[requires]
python_version = "3.x"
```

### API & Framework Documentations
- [Spotipy API][spotipy]
- [Tweepy API][tweepy]
- [IBM-Watson Tone Analyzer API][ibmwatson]
- [Preact, 3kb lightweight alternative to React][preact]





[repo]: https://github.com/tamargoadam/emotion-based-music-recommendation
[twitdev]: https://developer.twitter.com/
[spotdev]: https://developer.spotify.com/
[ibmdev]: https://cloud.ibm.com/registration?target=%2Fapidocs%2Ftone-analyzer
[spotipy]: https://spotipy.readthedocs.io/
[tweepy]: http://docs.tweepy.org/en/latest/
[ibmwatson]: https://cloud.ibm.com/apidocs/tone-analyzer
[pipenv]: https://pipenv-fork.readthedocs.io/en/latest/
[localhost]: http://localhost:8080/
[preact]: https://preactjs.com/
