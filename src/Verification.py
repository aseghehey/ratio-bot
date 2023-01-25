import tweepy

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
def isDeletedTweet(api, id):
    try:
        status(api, id)
        return False
    except tweepy.errors.TweepyException as err:
        return True

# checker to determine if there's ratio
def isRatio(tweetID,prevtweetID):
    return tweetID.favorite_count > prevtweetID.favorite_count

# given an ID, returns the status/tweet
def status(api, tweetID):
    return api.get_status(tweetID)