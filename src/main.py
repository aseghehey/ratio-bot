from Verification import *
from Auth import _get_auth_
from FileOperations import *
from Functionality import *
import time

if __name__ == "__main__":
    try:

        api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
    
        while True:
            print('started')
            replyratio(api, getLastSeen())
            time.sleep(1)

    except Exception as err:
        print(f'ERROR: {err}')
