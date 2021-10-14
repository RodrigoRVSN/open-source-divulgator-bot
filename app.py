import tweepy
import schedule
import time
import os


consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
acess_token = os.getenv('ACCESS_TOKEN')
acess_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(acess_token, acess_token_secret)
    api = tweepy.API(auth)
    schedule.every(10).minutes.do(retweet(api))

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_mentions(api):
    mentions = api.mentions_timeline()
    return mentions

def retweet(api):
    mentions = get_mentions(api)
    for mention in mentions:
        try:
            api.retweet(mention.id)
            print('Retweeted: ' + mention.text)
        except tweepy.TweepError as e:
            print(e.reason)


if __name__ == '__main__':
    main()