'''
MIT License

Copyright (c) 2022 Emanuel Aseghehey, Keonte Nightingale and Pratul Neupane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import tweepy
import time
import random
import heapq as hq
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def _get_auth_():
    auth = tweepy.OAuthHandler(os.getenv('ACCESS_KEY'),os.getenv('TWITTER_API_KEY'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_API_SECRET_KEY'))
    return auth

''' Tweet Verification/Validation '''
# check if tweet is protected because bot cant reply to those
def isProtected(tweet):
    if tweet.user.protected:
        return True
    return False

# required check otherwise crashes
def isValidTweet(tweet):
    for i in range(len(tweet.entities['user_mentions'])):
            if tweet.in_reply_to_screen_name in tweet.entities['user_mentions'][i]['screen_name']:
                return True
    return False

# if tweet no longer exists -> error
def isDeletedTweet(id):
    try:
        status(id)
        return False
    except tweepy.errors.TweepyException as err:
        return True

''' Functions: '''
def validateRatioFormat(tweet): # validates that there are two tweets above (correct format)
    if tweet.in_reply_to_status_id is not None: 
        if isValidTweet(tweet):
            tweet_2 = status(tweet.in_reply_to_status_id) 
            if not isProtected(tweet_2) and (tweet_2.in_reply_to_status_id is not None): 
                if isValidTweet(tweet_2):
                    tweet_1 = status(tweet_2.in_reply_to_status_id)
                    if not isProtected(tweet_1):
                        return True 
    return False

def validQuoteRatioFormat(mention):
    if mention.in_reply_to_status_id is not None:
        ratiotwt = status(mention.in_reply_to_status_id)
        if ratiotwt.is_quote_status and not isDeletedTweet(ratiotwt.quoted_status_id) :
            return True
    return False

'''
# gives random index from array: done by pratuln (his contribution)
def RSFromArray(Arr):
    Ridx = random.randint(0,len(Arr)-1)
    return Arr[Ridx]
'''

# given a textfile, return a random string from it
def readFromFile(filename):
    f_in = open(filename, 'r')
    messageArr = f_in.readlines()
    index = random.randrange(len(messageArr) - 1)
    f_in.close()
    return messageArr[index].replace('\n', '')

'''
# weekly wrapped

# maps to keep track of wins, losses and draws
wmap = {}
lmap = {}
dmap = {}

# Was planning on doing a weekly wrapped, where every Friday at 6pm, it would give the top3 users with Wins, Losses and Detections, however, twitter is not okay
# with mentioning people without them mentioning the bot first
# given a map (Win,Loss or Detect) the function returns a list of the top 3 things in the map
def weeklywrapped(givenmap):
    topRatios = []
    hq.heapify(topRatios)
    for key,val in givenmap.items():
        tmp = [val*-1,key]
        hq.heappush(topRatios, tmp)
    top3 = []
    # add checks to make sure its not out of bounds
    for i in range(3):
        top3.append(hq.heappop(topRatios))
    return top3

# creates the weekly message
def messageWeekly():
    #checks that map isnt empty and its length is greater than 3, otherwise we get an error
    if isMapEmpty(wmap) or len(wmap) < 3:
        return ""
    top3 = weeklywrapped(wmap)
    content = "top ratio accounts for this week 🔝\n\n"
    sayings = []
    for val, acc in top3:
        tmpuser = api.get_user(user_id=acc)
        tmp = f"@{tmpuser.screen_name} with {val*-1} ratio(s)"
        sayings.append(tmp)
    content += f"[🥇] {sayings[0]}\n[🥈] {sayings[1]}\n[🥉] {sayings[-1]}\n\nit resets every day at 6pm"
    return content

# takes the id of an account and returns their score in an array format: [Ws,Ls, Detections]
def acc_status(id): 
    resW,resL,resD = 0,0,0
    if id in wmap:
        resW = wmap[id]
    if id in lmap:
        resL = lmap[id]
    if id in dmap:
        resD = dmap[id]
    return [resW,resL,resD]

# would be used to determine when its time to post, but changed the function
# will now use it for when its 6pm, so bot clears map - for memory purposes
def timetopostWeekly():
    # post on fridays at 6pm
    dow = datetime.datetime.today().weekday()
    t = datetime.datetime.today().time().strftime("%H:%M:%S")
    if t == "18:00:00": #dow == 4 and 
        return True
    return False

# checks if the map is empty, would be used for the weekly wrapped, if i did it
def isMapEmpty(map):
    if not map:
        return True
    return False

# adding to map
def mapcount(id, RatioMap): # given an "id_str" will return count of that id
    if id not in RatioMap:
        RatioMap[id] = 1
    else:
        RatioMap[id] += 1
    return RatioMap[id]

#to clear all maps at once
def clearmaps():
    wmap.clear()
    lmap.clear()
    dmap.clear()

# adding to maps at once
def addToMaps(W,L,R):
    mapcount(W.user.id,wmap)
    mapcount(L.user.id,lmap)
    mapcount(R.user.id,dmap)

# would post weekly post but not doing it anymore
def makeWeeklypost():
    if messageWeekly()!="":
        api.update_status(messageWeekly())
        clearmaps()
'''

# posting a reply with picture
def reply_with_media(tweet_id, message, imagepath):
    api.update_status_with_media(message, imagepath, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

# posting a reply without picture
def reply_no_media(tweet_id,message):
    api.update_status(message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

# makes the format of the message, depending on what case it is
def messageFormat(id,option):
    content = ""
    if option == 1: # check ratio
        content = "✅ " + readFromFile('textfiles/messages/yesratio.txt')
    elif option == 4:# no ratio
        content =  readFromFile('textfiles/messages/noratio.txt')
    return content

    '''
        elif option == 2: #ratio account status
            stats = acc_status(id.user.id)
            content = f"@{id.user.screen_name} ratio status:\n\nWins: {stats[0]} ✅\nLosses: {stats[1]} ⬇️\nRatios reported: {stats[2]} 💯"
        elif option == 3: # incorrect format
            content = f"use the correct format\n\n@ me with 'check ratio' to report a ratio (anyone's) or 'ratio account status' to see your account's ratio score"
    '''

# checker to determine if there's ratio
def isRatio(tweetID,prevtweetID):
    return tweetID.favorite_count > prevtweetID.favorite_count

# given an ID, returns the status/tweet
def status(tweetID):
    return api.get_status(tweetID)

# functionality of the code
def sendTweet(mentionedtwt, ratiotwt, ratioedtwt):
    if isRatio(ratiotwt,ratioedtwt):
        # addToMaps(ratiotwt, ratioedtwt, mentionedtwt)
        message = messageFormat(ratioedtwt,1)
        # reply_with_media(mentionedtwt.id, message, readFromFile('textfiles/pictures/yesratio.txt'))
        print(f"RATIO {mentionedtwt.id}")
    else:
        message = messageFormat(mentionedtwt, 4)
        # reply_with_media(mentionedtwt.id, message, readFromFile('textfiles/pictures/noratio.txt'))
        print(f"NORATIO {mentionedtwt.id}")

''' Tweet ID text file '''
def set_last_seen(last_seen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(last_seen)
    f_write.close()
    return

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# needed
def _me_(tweet):
    botid = 1537546826026319872
    if tweet.user.id != botid:
        return False
    return True
 
'''
deprecated
def check_Android_L(tweet):
    if "Android" in tweet.source:
        return " + Twitter for Android 😭"
    return ""
'''

def whatRatioRequest(tweet):
    request1Set = {'check', 'ratio'}
    request2Set = {'account', 'status'}
    tweetArr = set([x.lower() for x in tweet.split(' ')])

    if request1Set.issubset(tweetArr):
        return 1
    elif request2Set.issubset(tweetArr):
        return 2

# execution of functionality
def replyratio(lastseen):
    mentionTimeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id

    for mention in reversed(mentionTimeline):
        #checks:
        if isProtected(mention) or isDeletedTweet(mention.id) or _me_(mention):
            print(f'INVALID_TWT_FORMAT: {mention}') 
            continue
        
        requestType = whatRatioRequest(mention.text)
        if requestType == 1: # found tweet
            if validateRatioFormat(mention):
                previousTweet = status(mention.in_reply_to_status_id)
                beforePrevious = status(previousTweet.in_reply_to_status_id)
                sendTweet(mention,previousTweet,beforePrevious)
            elif validQuoteRatioFormat(mention):
                ratioTweet = status(mention.in_reply_to_status_id)
                quoteTweet = status(ratioTweet.quoted_status_id_str)
                sendTweet(mention, ratioTweet, quoteTweet)
        elif requestType == 2:
            message = messageFormat(mention,2)
            # reply_no_media(mention.id_str,message)
            print(f'ACC_STATUS: {mention.id}')
        else:
            print(f'NO_REQ_MENTION {mention.id}')
    
        set_last_seen(mention.id_str, "textfiles/last_tweet.txt")

'''
# for testing purposes
def deleteMentions4testpurposes():
    t = api.user_timeline()
    for i,t1 in enumerate(t):
        if (t1.in_reply_to_status_id is not None) and (t1.in_reply_to_user_id != 1537546826026319872):
            api.destroy_status(t1.id)
'''

if __name__ == "__main__":
    try:
        api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
        replyratio(retrieve_last_seen_id("textfiles/last_tweet.txt"))
    except Exception as err:
        print(f'ERROR: {err}')