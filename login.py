import constants
import oauth2
from user import User
from database import Database
import json
import urllib.parse as urlparse
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


Database.initialise(user='postgres', password='password', host='localhost', database='learning')

user_email = input("Enter your e-mail address: ")

user = User.load_from_db_by_email(user_email)


if user:
    pass
else:

    request_token = user.get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    print("oauth " + str(access_token))

    email = input("Enter your email: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()


tweets = json.loads(user.twitter_request("https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images"))

for tweet in tweets['statuses']:
    print(tweet['text'])
# Create an 'authorized token' Token object and use that to perform Twitter API calls on behalf of the user


