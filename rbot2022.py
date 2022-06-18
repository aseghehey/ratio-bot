import tweepy

auth = tweepy.OAuthHandler("gRjwpFLL6vBrcHxCvodDP0625","GJRw9s10Vu8NalBvIvgU2nugQT92XZp5D9SXTybXSS2HJsZK9M")
auth.set_access_token("1537546826026319872-oJFAjAnSlHDHgEC1JIudZpERAG0H0w", "ZWhna4jAbMWan5sx2RlsEFGq50dsGOAYDzZ1kL6ado17Z" )

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("all good")
except:
    print("couldn't verify")

api.update_status("hello wrld: test #1")
# api.create_saved_search("tech")


# Client = tweepy.Client(consumer_key="qZfMbsC2DTI968j9uWxy3XFpj", consumer_secret="Q3GzTkPpccMA0ZatUi29UacXNJ1Aacmr2TuPi45jsBNTN2igtW", access_token="1537546826026319872-6HyHhzeSOKTgZ1dtbWokBpsUGWIx14",access_token_secret="RMS5c7ps7hbjQj9mGxrUvUuSq671RFjZkxAOtEhBlNYdZ")

# res = Client.create_tweet(text="hello wrld")
# print(res)

#testing that i can work on this project from my machine - Keonte Nightingale