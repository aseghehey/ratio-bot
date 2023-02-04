import random
 
def getRandomMessage(filename):
    f_in = open(filename, 'r')
    messageArr = f_in.readlines()
    index = random.randrange(len(messageArr))
    f_in.close()
    return messageArr[index].replace('\n', '')

''' Tweet ID text file '''
def writeLastSeen(content):
    f_write = open("assets/textfiles/last_tweet.txt", 'w')
    f_write.write(content)
    f_write.close()
    print(f'id written {content}')

def getLastSeen(): 
    f_read = open("assets/textfiles/last_tweet.txt", 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    print(f'id read: {last_seen_id}')
    return last_seen_id