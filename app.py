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
    schedule.every(10).minutes.do(retweet, api)

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_mentions(api):
    mentions = api.mentions_timeline()
    return mentions


def retweet(api):
    mentions = get_mentions(api)
    rt = Retweets()
    
    for mention in mentions:
        retweeted_mentions = rt.get_retweeted_mentions()
        try:
            if mention.id in retweeted_mentions:
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