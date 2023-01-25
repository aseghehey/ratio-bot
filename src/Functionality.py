from Verification import *
from FileOperations import *

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

def whatRatioRequest(tweet):
    request1Set = {'check', 'ratio'}
    request2Set = {'account', 'status'}
    tweetArr = set([x.lower() for x in tweet.split(' ')])

    if request1Set.issubset(tweetArr):
        return 1
    elif request2Set.issubset(tweetArr):
        return 2

# posting a reply with picture
def reply_with_media(api, tweet_id, message, imagepath):
    api.update_status_with_media(message, imagepath, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

# posting a reply without picture
def reply_no_media(api, tweet_id,message):
    api.update_status(message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

# functionality of the code
def sendTweet(mentionedtwt, ratiotwt, ratioedtwt):
    if isRatio(ratiotwt,ratioedtwt):
        # addToMaps(ratiotwt, ratioedtwt, mentionedtwt)
        message = getRandomMessage(f'textfiles/messages/yesratio.txt')
        try:
            # print(message)
            reply_with_media(mentionedtwt.id, message, getRandomMessage('textfiles/pictures/yesratio.txt'))
        except Exception as err:
            print('RWM1:',err)

        print(f"RATIO {mentionedtwt.id}")
    else:
        message = getRandomMessage(f'textfiles/messages/noratio.txt')
        try:
            # print(message)
            reply_with_media(mentionedtwt.id, message, getRandomMessage('textfiles/pictures/noratio.txt'))
        except Exception as err:
            print('RWM2:',err)

        print(f"NORATIO {mentionedtwt.id}")


def replyratio(api, lastseen):
    mentionTimeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id

    for mention in reversed(mentionTimeline):
        #checks:
        if isProtected(mention) or isDeletedTweet(mention.id): # or _me_(mention):
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
            # message = messageFormat(mention,2)
            # reply_no_media(mention.id_str,message)
            print(f'ACC_STATUS: {mention.id}')
        else:
            print(f'NO_REQ_MENTION {mention.id}')
    
        writeLastSeen(mention.id_str, "textfiles/last_tweet.txt")