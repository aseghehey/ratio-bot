from Verification import *
from FileOperations import *
import requests
import shutil
from pathlib import Path 
import os
from PIL import Image

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
    
# functionality of the code
def sendTweet(api, mentionedtwt, ratiotwt, ratioedtwt):
    if isRatio(ratiotwt, ratioedtwt):
        imageEdit(ratioedtwt)
        # print(f'ratio: {getRandomMessage("assets/textfiles/messages/yesratio.txt")}')
        api.update_status_with_media(getRandomMessage('assets/textfiles/messages/yesratio.txt'), "assets/pics/downloads/pic.jpg", in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)
        return
    api.update_status(getRandomMessage('assets/textfiles/messages/noratio.txt'), in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)


def replyratio(api, lastseen):
    mentionTimeline = api.mentions_timeline(since_id=lastseen) #since_id=last_seen_id

    for mention in reversed(mentionTimeline):
        #checks:
        if isProtected(mention) or isDeletedTweet(api, mention.id) or (not isRatioRequest(mention.text)): # or _me_(mention):
            continue
        
        if validateRatioFormat(api, mention):
            previousTweet = status(api, mention.in_reply_to_status_id)
            beforePrevious = status(api, previousTweet.in_reply_to_status_id)
            sendTweet(api, mention, previousTweet, beforePrevious)
        elif validQuoteRatioFormat(api, mention):
            ratioTweet = status(api, mention.in_reply_to_status_id)
            quoteTweet = status(api, ratioTweet.quoted_status_id_str)
            sendTweet(api, mention, ratioTweet, quoteTweet)    
        writeLastSeen(mention.id_str)

def profilePictureUrl(tweet):
    image_url = tweet.user.profile_image_url
    image_url = image_url[::-1]
    l, r = 0,1

    while r < len(image_url):
        if image_url[l] == '.' and image_url[r] == "_":
            break
        if image_url[l] != '.':
            l += 1
        r += 1

    new_url = image_url[:l + 1] + image_url[r + 1:]
    new_url = new_url[::-1]

    return new_url

def downloadProfilePic(url):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open('assets/pics/downloads/pic.jpg', 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        return True
    return False

def imageEdit(tweet):
    picpath = "assets/pics/downloads/pic.jpg"
    
    if (Path(picpath).is_file()):
        os.remove(picpath)

    downloadProfilePic(profilePictureUrl(tweet))
    image = Image.open(picpath)
    gradient = Image.open("assets/pics/edit/gradient.png")
    letter = Image.open("assets/pics/edit/L.png")
    
    # image = image.convert("L")
    image.paste(gradient,(0,0), gradient)
    image.paste(letter, (100,100), letter)
    image.save(picpath)