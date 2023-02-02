import tweepy

def isProtected(tweet):
    ''' check if tweet is protected because bot cant reply to those '''
    if tweet.user.protected:
        return True
    return False

# required check otherwise crashes
def isMentionedFormat(tweet):
    for i in range(len(tweet.entities['user_mentions'])):
            if tweet.in_reply_to_screen_name in tweet.entities['user_mentions'][i]['screen_name']:
                return True
    return False

def isValidTweet(api, id):
    '''
        This function checks against suspended and blocked accounts, and many others which may cause the bot
        to crash. The logic is to try access the given tweet, and if not possible, return False.
    '''
    try:
        status(api, id)
        return True
    except Exception as err:
        return False


def isRatio(tweetID,prevtweetID):
    ''' checker to determine if there's ratio '''
    return tweetID.favorite_count > prevtweetID.favorite_count

def status(api, tweetID):
    ''' given an ID, returns the status/tweet '''
    return api.get_status(tweetID)

def isRatioRequest(mentionText):
    ''' checker to ensure the key phrase was used for the request'''
    tweetSet = set([x.lower() for x in mentionText.split(' ')])
    reqSet = {'check', 'ratio'}
    return reqSet.issubset(tweetSet)

def validateRatioFormat(api, tweet):
    '''
        This function checks that the 3 tweets: mention, tweet1 (ratio), and tweet2 (ratio'd) are all valid
        and won't crash the bot
    '''
    print('RF: initiated')
    if isProtected(tweet) or (tweet.in_reply_to_status_id is None) or (not isValidTweet(api, tweet.in_reply_to_status_id)) or (not isMentionedFormat(tweet)):
        print('RF: false1')
        return [False, []]

    tweet_2 = status(api, tweet.in_reply_to_status_id) 
    if isProtected(tweet_2) or (tweet_2.in_reply_to_status_id is None) or (not isValidTweet(api, tweet_2.in_reply_to_status_id)) or (not isMentionedFormat(tweet_2)): 
        print('RF: false2')
        return [False, []]

    tweet_1 = status(api, tweet_2.in_reply_to_status_id)
    if isProtected(tweet_1):
        print('RF: false3')
        return [False, []]
    print('RF: true')
    return [True, [tweet_2, tweet_1]]

def validQuoteRatioFormat(api, mention):
    print('QF: initiated')
    if isProtected(mention) or (mention.in_reply_to_status_id is None) or (not isValidTweet(api, mention.in_reply_to_status_id)):
        print('QF: false1')
        return [False, []]

    ratiotwt = status(api, mention.in_reply_to_status_id)
    if (not ratiotwt.is_quote_status) or (not isValidTweet(api, ratiotwt.quoted_status_id)):
        print('QF: false2')
        return [False, []]
    ratiod = status(api, ratiotwt.quoted_status_id)
    print('QF: true')
    return [True, [ratiotwt, ratiod]]
    