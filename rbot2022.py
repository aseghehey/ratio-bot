from calendar import week
from cgi import test
import requests
import tweepy
import time
import random
import heapq as hq

def keys():
    auth = tweepy.OAuthHandler("gRjwpFLL6vBrcHxCvodDP0625","GJRw9s10Vu8NalBvIvgU2nugQT92XZp5D9SXTybXSS2HJsZK9M")
    auth.set_access_token("1537546826026319872-oJFAjAnSlHDHgEC1JIudZpERAG0H0w", "ZWhna4jAbMWan5sx2RlsEFGq50dsGOAYDzZ1kL6ado17Z" )
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
# WratioArr = ["ice cold ratio g", "outstanding ratio", "ratiooooo"]
# NoRatioArr = ["Stop wasting my time",""]
LratioArr = ["L + YB better", "hold this L", "ratio + L + get a job"]

# wmap = {"1537546826026319872":2134,"1906177190":1232,"1516168680660520962":11}
wmap = {}
lmap = {}
dmap = {}
ratiocounter = 1 

''' Functions: '''
def validateRatioFormat(tweet): # validates og and parent
    if tweet.in_reply_to_status_id is not None: # if it has a prev
        temp1 = api.get_status(tweet.in_reply_to_status_id) # create temp to check og
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
    for i in range(3):
        top3.append(hq.heappop(topRatios))
    return top3

def messageWeekly():
    if isMapEmpty(wmap):
        return "no ratios this week :("
        
    top3 = weeklywrapped(wmap)
    content = "top ratio accounts for this week 🔝\n\n"
    sayings = []
    for val, acc in top3:
        tmpuser = api.get_user(user_id=acc)
        tmp = f"@{tmpuser.screen_name} with {val*-1} ratio(s)"
        sayings.append(tmp)
    content += f"[🥇] {sayings[0]}\n[🥈] {sayings[1]}\n[🥉] {sayings[-1]}"
    return content

def makeWeeklypost():
    api.update_status(messageWeekly())

def reply_with_media(tweet_id, message, media):
    api.update_status_with_media(message,media,in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

def reply_no_media(tweet_id,message):
    api.update_status(message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

def messageformat(id,option):
    content = ""
    if option == 1: # check ratio
        content = f"✅ Ratio detected\n\n@{id.user.screen_name} {RSFromArray(LratioArr)}"
    elif option == 2: #ratio account status
        stats = acc_status(id.user.id)
        content = f"@{id.user.screen_name} ratio status:\n\nWins: {stats[0]} ✅\nLosses: {stats[1]} ⬇️\nRatios reported: {stats[2]} 💯"
    elif option == 3: # incorrect format
        content = f"stop wasting my time and use the correct format\n\n@ me with 'check ratio' to report a ratio (anyone's) or 'ratio account status' to see your account's ratio score"
    else:# no ratio
        content = "😐 Stop wasting my time"
    return content

def addToMaps(idW,idL,idR):
    mapcount(idW,wmap)
    mapcount(idL,lmap)
    mapcount(idR,dmap)

def replyratio():
    timeline = api.mentions_timeline()
    for mention in reversed(timeline):
        if "check ratio" in (mention.text).lower():
            if validateRatioFormat(mention):
                mention_id = mention.id
                prev_tweet = api.get_status(mention.in_reply_to_status_id)
                prevprev = api.get_status(prev_tweet.in_reply_to_status_id)
                if (prev_tweet.favorite_count) > (prevprev.favorite_count):
                    addToMaps(prev_tweet.user.id,prevprev.user.id,mention.user.id)
                    message = messageformat(prevprev,1)
                    reply_with_media(mention.id_str,message,"checkingratio.png")
                    # ratiocounter+=1 # to keep track of how many ratios we have found
                else: # no ratio
                    message = messageformat(mention,4)
                    reply_with_media(mention.id_str,message,"ratiodenied.jpeg")
        elif "ratio account status" in (mention.text).lower():
            message = messageformat(mention,2)
            reply_no_media(mention.id_str,message)
        else: # incorrect format
            message = messageformat(mention,3)
            reply_no_media(mention.id_str,message)

try:
    print("testing:\n")
    # print(messageWeekly())
    # print(isMapEmpty(wmap))
    print("\nWorks")
except Exception as err:
    print(err)

# "trash":

# api.update_status_with_media(f"✅ Ratio detected\n@ blank hold this L","checkingratio.png",in_reply_to_status_id=1538708496065101824)
# api.update_status_with_media(f"✅ Ratio detected\n@ blank hold this L","ratiodenied.jpeg",in_reply_to_status_id="1538708496065101824")
# api.update_status(f"✅ Ratio detected\n@ blank hold this L", in_reply_to_status_id=1538716509568131072, "checkingratio.png",auto_populate_reply_metadata=True)


# api.update_status("hello wrld 2",media_ids=1539070649615978500)
# trying to update status with media

# api.update_status_with_media("✅ Ratio detected\n@ blank hold this L","checkingratio.png")

# Need to get this to work properly:

'''
file_name = "last_tweet.txt"

def set_last_seen(last_seen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(mention_id))
    f_write.close()
    print('last seen set ' + str(mention_id))
    return

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    print('last seen found ' + str(last_seen_id))
    return last_seen_id

'''
# tweet id check 1538625211339313152


''' Cluster (contains while true with time '''
'''
while True:
    print(f"again w {mention_id}")
    # mentions = api.mentions_timeline(since_id = mention_id)
    replyratio()

    
    for mention in reversed(mentions):
        try:
            mention_id = mention.id

            # print("trying") 
            if validate(mention):
                # print("valid format")
                # get above tweets
                prev_tweet = api.get_status(mention.in_reply_to_status_id)
                prevprev = api.get_status(prev_tweet.in_reply_to_status_id)
                
                # Testing:
                print(f"{ratiocounter} - {prev_tweet.user.screen_name} - {prev_tweet.text} - {mention.id} - {prev_tweet.user.id}")

                #Compare like counts
                if (prev_tweet.favorite_count) > (prevprev.favorite_count):
                    wmapcnt = mapcount(prev_tweet.user.id,wmap)
                    lmapcnt = mapcount(prevprev.user.id,lmap)
                    print(f"ratio {ratiocounter} w {wmapcnt}, l {lmapcnt}")
                    # api.update_status(f"#{ratiocounter} @{prev_tweet.user.screen_name} ratiod @{prevprev.user.screen_name}", in_reply_to_status_id=mention.id_str,auto_populate_reply_metadata=True)
                    ratiocounter+=1 
                else:
                    print("no ratio")
                    # api.update_status("Stop wasting my time", in_reply_to_status_id=mention.id_str,auto_populate_reply_metadata=True)
                print("success")
            
            # something sassy if format is invalid
        except Exception as err:
            print(err)
    

    time.sleep(15) # reloads mentions every 15 seconds

'''
'''
while True:
    mentions = api.mentions_timeline(since_id=mention_id) # gets a timeline of mentions
    for mention in mentions: # will go through each mention
        print(mention.text)
        if (mention.text.lower().find("ratio status")) != -1:
        # if (mention.text).find("ratio status") != -1: # if contains "ratio status"
            try:
                api.retweet(mention.id)
                print("sucessfully retweeted")
            except Exception as err:
                print(err)
        else:
            print("doesn't contain ratio status...")

            # pass # reply to the tweet with the ratio analysis
        mention_id = mention.id # sets m_id to current, so it doesnt read the same mention again
    time.sleep(15) # reloads mentions every 15 seconds
'''
'''
while True:
    mentions = api.mentions_timeline(since_id=mention_id) # gets a timeline of mentions
    for mention in mentions: # will go through each mention
        print(mention.author.screen_name,mention.text)
        mention_id = mention.id
        if (mention.text.lower().find("ratio status")) != -1:
        # if (mention.text).find("ratio status") != -1: # if contains "ratio status"
            # print(mention.id_str)
            api.update_status("checking ratio hollon son", in_reply_to_status_id=mention.id_str,auto_populate_reply_metadata=True)
            # try:
            #     print("trying to reply")
            #     api.update_status("Checking possible ratio...", in_reply_to_status_id=mention.id_str)
            #     print("sucessfully replied")
            # except Exception as err:
            #     print(err)
        else:
            print("doesn't contain ratio status... so won't reply")
        # mention_id = mention.id # sets m_id to current, so it doesnt read the same mention again
    time.sleep(15) # reloads mentions every 15 seconds

'''
