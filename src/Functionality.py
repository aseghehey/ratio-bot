from Verification import *
from FileOperations import *
import requests
import shutil
from pathlib import Path 
import os
from PIL import Image

def sendTweet(api, mentionedtwt, ratiotwt, ratioedtwt):
    '''
        This function is used to post the tweet reply.
    '''
    print('sendTweetOn')
    if isRatio(ratiotwt, ratioedtwt):
        imageEdit(ratioedtwt)
        # print(f'ratio: {getRandomMessage("assets/textfiles/messages/yesratio.txt")}')
        print(f'UI {ratiotwt.id_str} {ratioedtwt.id_str}')
        # api.update_status_with_media(getRandomMessage('assets/textfiles/messages/yesratio.txt'), "assets/pics/downloads/pic.jpg", in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)
        return
    print(f'UNI {ratiotwt.id_str} {ratioedtwt.id_str}')
    # api.update_status(getRandomMessage('assets/textfiles/messages/noratio.txt'), in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)


def replyratio(api, lastseen):
    '''
        This function goes through the mentions timeline, and checks the ratios.
    '''

    mentionTimeline = api.mentions_timeline(since_id=lastseen) # accessing the timeline since the last seen id
    for mention in reversed(mentionTimeline): # removed reverse()

        print(f'at {mention.id_str}')
        #checks:
        if isProtected(mention) or (not isValidTweet(api, mention.id)) or (not isRatioRequest(mention.text)):
            print(f'FAIL CHECK')
            continue
        
        normalFormat = validateRatioFormat(api, mention)
        quoteFormat = validQuoteRatioFormat(api, mention)

        if (not normalFormat[0]) and (not quoteFormat[0]):
            print('NO FORMAT')
            continue

        if normalFormat[0]:
            print('NORMAL FORMAT')   
            previousTweet = normalFormat[1][0]
            beforePrevious = normalFormat[1][1]
        else:
            print('QUOTE FORMAT')
            previousTweet = quoteFormat[1][0]
            beforePrevious[1][1]
        sendTweet(api, mention, previousTweet, beforePrevious)  
        writeLastSeen(mention.id_str)

def profilePictureUrl(tweet):
    '''
        Refer to Twitter's profile picture guidelines. This function performs necessary operations to get the 
        400 x 400 profile picture size and returns that url.
    '''

    image_url = tweet.user.profile_image_url
    image_url = image_url[::-1]
    l, r = 0,1
    while r < len(image_url):
        if image_url[l] == '.' and image_url[r] == "_":
            break
        if image_url[l] != '.':
            l += 1
        r += 1
    add = "_400x400"[::-1]
    new_url = image_url[:l + 1] + add + image_url[r + 1:]
    new_url = new_url[::-1]
    print('Url operation done sucessfully')
    return new_url

def downloadProfilePic(url):
    '''
        Given a url, this function downloads the image associated with the url.
        It saves it to the downloads folder 
    '''
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open('assets/pics/downloads/pic.jpg', 'wb') as f:
            shutil.copyfileobj(res.raw, f)
    print('Downloaded image successfully')

def imageEdit(tweet):
    ''' 
        This method will check if there's an image in the assets/pics/downloads/
        and delete it, because there can only ever be one image. Then it will download the users profile pic,
        and perform the addition of the two objects, and save it.
    '''

    picpath = "assets/pics/downloads/pic.jpg" # location of image    
    if (Path(picpath).is_file()):
        os.remove(picpath)
    downloadProfilePic(profilePictureUrl(tweet)) 
    image = Image.open(picpath) 
    gradient = Image.open("assets/pics/edit/gradient.png") 
    letter = Image.open("assets/pics/edit/L.png") 
    ''' Pasting objects onto image and saving it in desired folder '''
    image.paste(gradient,(0,0), gradient)
    image.paste(letter, (100,100), letter)
    image.save(picpath)

    print('Image done succesfully')