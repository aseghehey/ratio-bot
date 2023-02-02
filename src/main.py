from Verification import *
from Auth import _get_auth_
from FileOperations import *
from Functionality import *
import time

if __name__ == "__main__":
    try:

        api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
        while True:
            last_id = getLastSeen()
            replyratio(api, last_id)
            time.sleep(15)
    except Exception as err:
        print(f'ERROR: {err}')
