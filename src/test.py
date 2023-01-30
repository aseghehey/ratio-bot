from Auth import _get_auth_
from Verification import status
import tweepy
import requests
import shutil
from pathlib import Path 
import os
from PIL import Image

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
        with open('/Users/emanuelaseghehey/Development/Ratio-bot/src/assets/pics/downloads/pic.jpg', 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        return True
    return False

if __name__ == "__main__":

    picpath = "/Users/emanuelaseghehey/Development/Ratio-bot/src/assets/pics/downloads/pic.jpg"
    if (Path(picpath).is_file()):
        os.remove(picpath)

    api = tweepy.API(_get_auth_(), wait_on_rate_limit=True)
    test = status(api, 1602229560342630400)
    downloadProfilePic(profilePictureUrl(test))

    read_image = Image.open(picpath)
    # read_image = read_image.convert('L')
    read_image.save(picpath)
    l = Image.open("/Users/emanuelaseghehey/Development/Ratio-bot/src/L.png")

    read_image.paste(l, (100,100), mask=l)
    read_image.show()

