from Verification import *
from Auth import _get_auth_
from FileOperations import *
from Functionality import *
import time

# 1602030942855393282 dnw
# 1597307437304131584 works


# 1540416388195442688 first

api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
# t = status(api, 1597269093001953282)
# mt = api.mentions_timeline(trim_user=True)
# print(mt[::-1][0])

t = status(api, 1598009735420137472)
validQuoteRatioFormat(api, t)