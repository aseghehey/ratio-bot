from calendar import week
from cgi import test
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
WratioArr = ["ice cold ratio", "outstanding ratio", "ratiooooo", "ratio detected!","W", "dub","fire ratio", "VAR DECISION: ratio", "ratio identified + W", "we have uncovered a remarkable ratio"]
NoRatioArr = ["stop wasting my time there's no ratio as of rn 🙄","stop being silly 😐", "no ratio as of rn 😕", "no ratio found 😒","come on there's no ratio there... 😐"]
LratioArr = ["L + ratio + YB better", "hold this L", "ratio + L + get a job", "ratiooood","hold this L respectfully", "respectfully ratio + L", "down bad", "down horrendoulsy", "argument: invalid + ratio"]

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

def makeWeeklypost():
    if messageWeekly()!="":
        api.update_status(messageWeekly())

def reply_with_media(tweet_id, message, media):
    api.update_status_with_media(message,media,in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

def reply_no_media(tweet_id,message):
    api.update_status(message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

def messageformat(id,option):
    content = ""
    if option == 1: # check ratio
        content = f"{RSFromArray(WratioArr)} ✅\n\n@{id.user.screen_name} {RSFromArray(LratioArr)}"
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
        reply_with_media(mentionedtwt.id_str,message,"checkingratio.png")
    else:
        # mapcount(mentionedtwt.user.id,lmap) #not necessary
        message = messageformat(mentionedtwt,4)
        reply_with_media(mentionedtwt.id_str,message,"ratiodenied.jpeg")

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

def replyratio(lastseen):
    # last_seen_id = retrieve_last_seen_id(file_name)
    timeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id
    for mention in reversed(timeline):
        # set_last_seen(mention.id_str,file_name)
        set_last_seen(mention.id_str,file_name)
        if "check ratio" in (mention.text).lower():
            if validateRatioFormat(mention): # if regular format
                # mention_id = mention.id
                prev_tweet = status(mention.in_reply_to_status_id)
                prevprev = status(prev_tweet.in_reply_to_status_id)
                applyRatio(mention,prev_tweet,prevprev)
            elif validQuoteRatioFormat(mention): # if quote tweet format
                ratio = status(mention.in_reply_to_status_id)
                quote = status(ratio.quoted_status_id_str)
                applyRatio(mention,ratio,quote)
        elif "ratio account status" in (mention.text).lower():
            message = messageformat(mention,2)
            reply_no_media(mention.id_str,message)
        else: # incorrect format
            message = messageformat(mention,3)
            reply_no_media(mention.id_str,message)

def deleteMentions4testpurposes():
    t = api.user_timeline()
    for i,t1 in enumerate(t):
        if (t1.in_reply_to_status_id is not None) and (t1.in_reply_to_user_id != 1537546826026319872):
            api.destroy_status(t1.id)

try:
    print("trying")
    # deleteMentions4testpurposes()
    # while True:
    #     replyratio(retrieve_last_seen_id(file_name))
    #     time.sleep(15)
    print("done")
except Exception as err:
    print(err)

# while True:
#     try:
#         print("testing:\n")
#         # retrieve_last_seen_id(file_name)
#         # replyratio()
#         print("\nWorks")
#         time.sleep(15)
#     except Exception as err:
#         print(err)

# "trash":

# api.update_status_with_media(f"✅ Ratio detected\n@ blank hold this L","checkingratio.png",in_reply_to_status_id=1538708496065101824)
# api.update_status_with_media(f"✅ Ratio detected\n@ blank hold this L","ratiodenied.jpeg",in_reply_to_status_id="1538708496065101824")
# api.update_status(f"✅ Ratio detected\n@ blank hold this L", in_reply_to_status_id=1538716509568131072, "checkingratio.png",auto_populate_reply_metadata=True)


# api.update_status("hello wrld 2",media_ids=1539070649615978500)
# trying to update status with media

# api.update_status_with_media("✅ Ratio detected\n@ blank hold this L","checkingratio.png")

# Need to get this to work properly:

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
