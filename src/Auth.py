import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

def _get_auth_():
    auth = tweepy.OAuthHandler(os.getenv('ACCESS_KEY'),os.getenv('TWITTER_API_KEY'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_API_SECRET_KEY'))
    return auth