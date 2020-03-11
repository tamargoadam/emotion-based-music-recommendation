# Testing the endpoints
Clone and enter project repo
```
git clone https://github.com/tamargoadam/emotion-based-music-recommendation.git
cd emotion-based-music-recommendation
```
install dependency manager and dependencies 
(pipenv allows us to manage dependencies)
```
pip install --user pipenv
pipenv install
```
pipenv should've installed the necessary libraries (pandas, tweepy, etc...). now use pipenv to create a virtualenv and run a script.
```
pipenv shell
python3 twitter_popularsearch.py
```

# extract credentials.zip
unzip credentials.zip
