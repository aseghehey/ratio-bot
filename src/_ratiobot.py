from Verification import *
from Auth import _get_auth_
from FileOperations import *
from Functionality import *

if __name__ == "__main__":
    try:

        api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
        # replyratio(getLastSeen("textfiles/last_tweet.txt"))


        # test
        # ob1 = status(api, 1618048774437490688)
        # print(ob1.in_reply_to_status_id_str)
        # print(ob1.entities['user_mentions'][1]['id_str'])

    except Exception as err:
        print(f'ERROR: {err}')