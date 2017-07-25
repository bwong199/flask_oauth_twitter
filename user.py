from database import CursorFromConnectionPool
import oauth2
from twitter_utils import consumer
import json

class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id=None):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    def save_to_db(self):
        # This is creating a new connection pool every time! Very expensive...
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                            (self.screen_name, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionPool() as cursor:
            # Note the (email,) to make it a tuple!
            cursor.execute('SELECT * FROM users WHERE screen_name=%s', (screen_name,))
            user_data = cursor.fetchone()
            print(user_data)
            if user_data:
                return cls(screen_name=user_data[1],
                           oauth_token=user_data[2], oauth_token_secret=user_data[3], id=user_data[0])


    def twitter_request(self, uri, verb="GET"):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # Make TWitter API call
        response, content = authorized_client.request(
            uri, verb)
        print(response.status)
        print(json.loads(content.decode('utf-8')))
        if response.status != 200:
            print("An error occurred when searching!")
        return json.loads(content.decode('utf-8'))



