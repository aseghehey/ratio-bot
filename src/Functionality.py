from Verification import *
from FileOperations import *

def validateRatioFormat(api, tweet):
    if tweet.in_reply_to_status_id is not None:  
        if isValidTweet(tweet):
            tweet_2 = status(api, tweet.in_reply_to_status_id) 
            if not isProtected(tweet_2) and (tweet_2.in_reply_to_status_id is not None): 
                if isValidTweet(tweet_2):
                    tweet_1 = status(api, tweet_2.in_reply_to_status_id)
                    if not isProtected(tweet_1):
                        return True 
    return False

def validQuoteRatioFormat(api, mention):
    if mention.in_reply_to_status_id is not None:
        ratiotwt = status(api, mention.in_reply_to_status_id)
        if ratiotwt.is_quote_status and not isDeletedTweet(api, ratiotwt.quoted_status_id):
            return True
    return False
    
# api.update_status(api, message, in_reply_to_status_id=tweet_id,auto_populate_reply_metadata=True)

# functionality of the code
def sendTweet(api, mentionedtwt, ratiotwt, ratioedtwt):
    if isRatio(ratiotwt, ratioedtwt):
        message = getRandomMessage(f'src/assets/textfiles/messages/yesratio.txt')
        imagepath = getRandomMessage('src/assets/textfiles/pictures/yesratio.txt')
        print(message, imagepath, mentionedtwt.id)
        # api.update_status_with_media(message, imagepath, in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)
    else:
        message = getRandomMessage(f'src/assets/textfiles/messages/noratio.txt')
        imagepath = getRandomMessage('src/assets/textfiles/pictures/noratio.txt')
        print(message, imagepath, mentionedtwt.id)
        # api.update_status_with_media(message, imagepath, in_reply_to_status_id=mentionedtwt.id, auto_populate_reply_metadata=True)

def replyratio(api, lastseen):
    mentionTimeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id

    for mention in reversed(mentionTimeline):
        #checks:
        if isProtected(mention) or isDeletedTweet(api, mention.id): # or _me_(mention):
            continue
        
        if validateRatioFormat(mention):
            previousTweet = status(api, mention.in_reply_to_status_id)
            beforePrevious = status(api, previousTweet.in_reply_to_status_id)
            sendTweet(api, mention, previousTweet, beforePrevious)
        elif validQuoteRatioFormat(mention):
            ratioTweet = status(api, mention.in_reply_to_status_id)
            quoteTweet = status(api, ratioTweet.quoted_status_id_str)
            sendTweet(api, mention, ratioTweet, quoteTweet)    
        writeLastSeen(mention.id_str, "textfiles/last_tweet.txt")