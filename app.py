import tweepy
import schedule
import time
import os

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
acess_token = os.getenv('ACCESS_TOKEN')
acess_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
ret_mentions = []


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(acess_token, acess_token_secret)
    api = tweepy.API(auth)
    schedule.every(30).minutes.do(retweet, api)

    while True:
        schedule.run_pending()
        time.sleep(1)

def binarySearch(arr, l, r, x):
    while l <= r:
        mid = l + (r - l) // 2;

        if arr[mid] == x:
            return True
 
        elif arr[mid] < x:
            l = mid + 1
 
        else:
            r = mid - 1
            
    return -1

def linearSearch(arr, value):
    if value in arr:
        return True
    return False   


def is_retweeted(mention_id, ret_mentions):
    if len(ret_mentions) < 20:
        return linearSearch(ret_mentions, mention_id)
    return binarySearch(ret_mentions, 0, len(ret_mentions) - 1, mention_id)


def get_mentions(api):
    mentions = api.mentions_timeline()
    return mentions


def retweet(api):
    mentions = get_mentions(api)
    rt = Retweets()
    
    for mention in mentions:
        retweeted_mentions = rt.get_retweeted_mentions()
        try:
            if is_retweeted(mention.id, retweeted_mentions) == True:
                continue
            else:
                api.retweet(mention.id)
                print('Retweeted: ' + mention.text)
                rt.add_retweet(mention.id)
                

        except tweepy.TweepError as e:
            print(e.reason)

class Retweets:
    def __init__(self, retweeted_mentions=ret_mentions):
        self.retweeted_mentions = ret_mentions
    
    def add_retweet(self, mention):
        self.retweeted_mentions.append(mention)

    def get_retweeted_mentions(self):
        return self.retweeted_mentions


if __name__ == '__main__':
    main()