from curses import KEY_EOL
from turtle import clear
import tweepy
import time
import random
import heapq as hq
import datetime
from dotenv import load_dotenv
import os
from keep_alive import keep_alive

def keys():
    load_dotenv()
    auth = tweepy.OAuthHandler(os.getenv('key_1'),os.getenv('key_2'))
    auth.set_access_token(os.getenv('key_3'),os.getenv('key_4'))
    return auth

api = tweepy.API(keys())

# verification
try:
    api.verify_credentials()
    print("verified")
except:
    print("couldn't verify")

mention_id = 1 # will be used to keep track of the mentions we have gone through

''' Variables: '''
# Arrays for guy who ratiod, guy who got ratiod and for no ratio found
WratioArr = ["ice cold ratio", "outstanding ratio", "ratiooooo", "ratio detected!","W", "dub","fire ratio", "VAR DECISION: ratio", "ratio identified + W", "we have uncovered a remarkable ratio"]
NoRatioArr = ["stop wasting my time there's no ratio as of rn 🙄","stop being silly 😐", "no ratio as of rn 😕", "no ratio found 😒","come on there's no ratio there... 😐"]
LratioArr = ["L + ratio + YB better", "hold this L", "ratio + L + get a job", "ratiooood","hold this L respectfully", "ratio + L", "down bad", "down horrendoulsy", "invalid argument + ratio"]

# wmap = {"1537546826026319872":2134,"1906177190":1232,"1516168680660520962":11}
wmap = {}
lmap = {}
dmap = {}
ratiocounter = 1 

''' Functions: '''
def validateRatioFormat(tweet): # validates og and parent
    if tweet.in_reply_to_status_id is not None: # if it has a prev
        temp1 = status(tweet.in_reply_to_status_id) # create temp to check og
        if temp1.in_reply_to_status_id is not None: # if og exists
            return True 
    return False

def isMapEmpty(map):
    if not map:
        return True
    return False

def mapcount(id, RatioMap): # given an "id_str" will return count of that id
    if id not in RatioMap:
        RatioMap[id] = 1
    else:
        RatioMap[id] += 1
    return RatioMap[id]

def acc_status(id): 
# takes the id of an account and returns their score in an array format: [Ws,Ls, Detections]
    resW,resL,resD = 0,0,0
    if id in wmap:
        resW = wmap[id]
    if id in lmap:
        resL = lmap[id]
    if id in dmap:
        resD = dmap[id]
    return [resW,resL,resD]

def RSFromArray(Arr):
    Ridx = random.randint(0,len(Arr)-1)
    return Arr[Ridx]

def weeklywrapped(givenmap):
    # given a map (Win,Loss or Detect) the function returns a list of the top 3 things in the map
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
    content += f"[🥇] {sayings[0]}\n[🥈] {sayings[1]}\n[🥉] {sayings[-1]}"
    return content

def timetopostWeekly():
    # post on fridays at 6pm
    dow = datetime.datetime.today().weekday()
    t = datetime.datetime.today().time().strftime("%H:%M:%S")
    if dow == 4 and (t == "18:00:03"):
        return True
    return False

# def testpost():
#     if timetopostWeekly():
#         api.update_status("posted today at 22:21:00")

def clearmaps():
    wmap.clear()
    lmap.clear()
    dmap.clear()

def makeWeeklypost():
    if messageWeekly()!="":
        api.update_status(messageWeekly())
        clearmaps()

def reply_with_media(tweet_id, message, media):
    api.update_status_with_media(message,media,in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True) #,auto_populate_reply_metadata=True
    print("tweeted with media")

def reply_no_media(tweet_id,message):
    api.update_status(message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)
    print("tweeted no media")

def messageformat(id,option):
    content = ""
    if option == 1: # check ratio
        content = f"{RSFromArray(WratioArr)} 🐐✅\n@{id.user.screen_name} {RSFromArray(LratioArr)}"
    elif option == 2: #ratio account status
        stats = acc_status(id.user.id)
        content = f"@{id.user.screen_name} ratio status:\n\nWins: {stats[0]} ✅\nLosses: {stats[1]} ⬇️\nRatios reported: {stats[2]} 💯"
    elif option == 3: # incorrect format
        content = f"use the correct format\n\n@ me with 'check ratio' to report a ratio (anyone's) or 'ratio account status' to see your account's ratio score"
    else:# no ratio
        content = f"{RSFromArray(NoRatioArr)}"
    return content

def addToMaps(W,L,R):
    mapcount(W.user.id,wmap)
    mapcount(L.user.id,lmap)
    mapcount(R.user.id,dmap)

def calculateratio(tweetID,prevtweetID):
    if tweetID.favorite_count > prevtweetID.favorite_count:
        return True
    else:
        return False

def status(tweetID):
    return api.get_status(tweetID)

def validQuoteRatioFormat(mention):
    if mention.in_reply_to_status_id is not None:
        ratiotwt = status(mention.in_reply_to_status_id)
        if ratiotwt.is_quote_status:
            return True
    return False

def applyRatio(mentionedtwt, ratiotwt, ratioedtwt):
    if calculateratio(ratiotwt,ratioedtwt):
        addToMaps(ratiotwt,ratioedtwt,mentionedtwt)
        message = messageformat(ratioedtwt,1)
        # reply_with_media(mentionedtwt.id,message,"checkingratio.png")
        reply_no_media(mentionedtwt.id,message)
    else:
        # mapcount(mentionedtwt.user.id,lmap) #not necessary
        message = messageformat(mentionedtwt,4)
        reply_no_media(mentionedtwt.id,message)
        # reply_with_media(mentionedtwt.id,message,"ratiodenied.jpeg")

file_name = "last_tweet.txt"
def set_last_seen(last_seen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(last_seen)
    f_write.close()
    print(f"last seen set: {last_seen}")
    return

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    print(f"last seen found {last_seen_id}")
    return last_seen_id

botid = 1537546826026319872

def replyratio(lastseen):
    # last_seen_id = retrieve_last_seen_id(file_name)
    timeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id
    for mention in reversed(timeline):
        # set_last_seen(mention.id_str,file_name)
        set_last_seen(mention.id_str,file_name)
        if mention.author.id != 1537546826026319872:
            if "check ratio" in (mention.text).lower():
                if validateRatioFormat(mention):
                    prev_tweet = status(mention.in_reply_to_status_id)
                    prevprev = status(prev_tweet.in_reply_to_status_id)
                    applyRatio(mention,prev_tweet,prevprev)
                elif validQuoteRatioFormat(mention):
                    ratio = status(mention.in_reply_to_status_id)
                    quote = status(ratio.quoted_status_id_str)
                    applyRatio(mention,ratio,quote)
            elif "ratio account status" in (mention.text).lower():
                message = messageformat(mention,2)
                reply_no_media(mention.id_str,message)
            else: # incorrect format
                check1 = status(mention.in_reply_to_status_id)
                print(check1.user.id)
                if check1.user.id != 1537546826026319872:
                    message = messageformat(mention,3)
                    reply_no_media(mention.id_str,message)

def deleteMentions4testpurposes():
    t = api.user_timeline()
    for i,t1 in enumerate(t):
        if (t1.in_reply_to_status_id is not None) and (t1.in_reply_to_user_id != 1537546826026319872):
            api.destroy_status(t1.id)

def main():
    try:
        print("trying")
        keep_alive()
        # reply_no_media("1539573736126431232","hi @elonhireme_")

        # print(datetime.datetime.today().time())
        # print()
        # deleteMentions4testpurposes()
        while True:
             if timetopostWeekly():
                 makeWeeklypost()
            
             replyratio(retrieve_last_seen_id(file_name))
             time.sleep(15)
        print("done")
    except Exception as err:
        print(err)
main()
