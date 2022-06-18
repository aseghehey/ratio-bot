import tweepy
import time

auth = tweepy.OAuthHandler("gRjwpFLL6vBrcHxCvodDP0625","GJRw9s10Vu8NalBvIvgU2nugQT92XZp5D9SXTybXSS2HJsZK9M")
auth.set_access_token("1537546826026319872-oJFAjAnSlHDHgEC1JIudZpERAG0H0w", "ZWhna4jAbMWan5sx2RlsEFGq50dsGOAYDzZ1kL6ado17Z" )

api = tweepy.API(auth)

# verification
try:
    api.verify_credentials()
    print("all good")
except:
    print("couldn't verify")

# api.update_status("hello wrld: test #1")
# api.create_saved_search("tech")

# has to contain "ratio status"
# example: @ratio_bot_2022 ratio status
# bot_id = int(api.me().id_str) 
mention_id = 1
# bot replying to its mentions which contain "ratio this"
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
