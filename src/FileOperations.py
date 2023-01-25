import random
 
def getRandomMessage(filename):
    f_in = open(filename, 'r')
    messageArr = f_in.readlines()
    index = random.randrange(len(messageArr) - 1)
    f_in.close()
    return messageArr[index].replace('\n', '')

''' Tweet ID text file '''
def writeLastSeen(content):
    f_write = open("src/assets/textfiles/last_tweet.txt", 'w')
    f_write.write(content)
    f_write.close()

def getLastSeen():
    f_read = open("src/assets/textfiles/last_tweet.txt", 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id