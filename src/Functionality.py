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
    print('::::::::: sendTweetOn :::::::::')
    if isRatio(ratiotwt, ratioedtwt):
        if imageEdit(ratioedtwt):
            api.update_status_with_media(getRandomMessage('assets/textfiles/messages/yes2ratio.txt'), "assets/pics/downloads/pic.jpg", in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)
            print(f'::::::::: UI1 {ratiotwt.id_str} {ratioedtwt.id_str} :::::::::')
        else:
            api.update_status_with_media(getRandomMessage('assets/textfiles/messages/yesratio.txt'), getRandomMessage("assets/textfiles/pictures/yesratio.txt"), in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)
            print(f'::::::::: UI2 {ratiotwt.id_str} {ratioedtwt.id_str} :::::::::')
        return
    api.update_status_with_media(getRandomMessage('assets/textfiles/messages/noratio.txt'), getRandomMessage("assets/textfiles/pictures/noratio.txt"), in_reply_to_status_id= mentionedtwt.id, auto_populate_reply_metadata=True)
    print(f'::::::::: UNI {ratiotwt.id_str} {ratioedtwt.id_str} :::::::::')

def replyratio(api, lastseen):
    '''
        This function goes through the mentions timeline, and checks the ratios.
    '''
    print('::::::::: on replyRatio :::::::::')
    mentionTimeline = api.mentions_timeline(since_id=lastseen) # accessing the timeline since the last seen id
    for mention in reversed(mentionTimeline): # removed reverse()
        writeLastSeen(mention.id_str)
        print(f'::::::::: @ {mention.id_str} :::::::::')
        #checks:
        if isProtected(mention) or (not isValidTweet(api, mention.id)) or (not isRatioRequest(mention.text)) or (mention.user.id == 1537546826026319872):
            print(f'::::::::: FAIL CHECK :::::::::')
            continue
        
        normalFormat = validateRatioFormat(api, mention)
        
        if normalFormat[0]:
            print('::::::::: COMMENT FORMAT :::::::::')   
            previousTweet = normalFormat[1][0]
            beforePrevious = normalFormat[1][1]
            sendTweet(api, mention, previousTweet, beforePrevious)  
        else:
            quoteFormat = validQuoteRatioFormat(api, mention) 

            if not quoteFormat[0]:
                continue

            print('::::::::: QUOTE FORMAT :::::::::')
            previousTweet = quoteFormat[1][0]
            beforePrevious = quoteFormat[1][1]
            sendTweet(api, mention, previousTweet, beforePrevious)  

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
    print(f'::::::::: URL {new_url} :::::::::')
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
    print('::::::::: Downloaded image successfully :::::::::')

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

    if (image.size != (400,400)):
        return False

    gradient = Image.open("assets/pics/edit/gradient.png") 
    letter = Image.open("assets/pics/edit/L.png") 
    ''' Pasting objects onto image and saving it in desired folder '''

    try:
        image.paste(gradient,(0,0), gradient)
        image.paste(letter, (100,100), letter)
        image.save(picpath)
        print('::::::::: Image edit success :::::::::')
        return True
    except Exception as e:
        print("::::::::: Image edit failed :::::::::")
        return False