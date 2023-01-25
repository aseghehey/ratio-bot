from Verification import *
from Auth import _get_auth_
from FileOperations import *
from Functionality import *

if __name__ == "__main__":
    try:

        api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
        replyratio(getLastSeen("textfiles/last_tweet.txt"))

    except Exception as err:
        print(f'ERROR: {err}')