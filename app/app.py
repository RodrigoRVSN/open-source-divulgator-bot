from pandas.core.series import Series
import tweepy
import schedule
import time
import os
import pandas as pd
import search

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
acess_token = os.getenv('ACCESS_TOKEN')
acess_token_secret = os.getenv('ACCESS_TOKEN_SECRET')


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(acess_token, acess_token_secret)
    api = tweepy.API(auth)
    schedule.every(30).minutes.do(retweet, api)

    while True:
        schedule.run_pending()
        time.sleep(1)

def retweet(api):
    mentions = get_mentions(api)
    for mention in mentions:
        retweeted_mentions = list(get_retweeted_mentions()['id'])
        try:
            if is_retweeted(mention.id, retweeted_mentions) == True:
                continue
            else:
                api.retweet(mention.id)
                print('Retweeted: ' + mention.text)
                add_retweet(mention.id)
            
        except tweepy.TweepError as e:
            print(e.reason)


def is_retweeted(mention_id, ret_mentions):
    if len(ret_mentions) < 20:
        return search.linearSearch(ret_mentions, mention_id)
    return search.binarySearch(ret_mentions, 0, len(ret_mentions) - 1, mention_id)

def get_mentions(api):
    mentions = api.mentions_timeline()
    return mentions

def add_retweet(mention):
    ret_mentions = get_retweeted_mentions()
    row = pd.Series(mention, index=['id'])
    ret_mentions = ret_mentions.append(row, ignore_index=True)
    ret_mentions.to_csv('/retweeted_mentions/ret_mentions.csv', index=False)

def get_retweeted_mentions():
    ret_mentions = pd.read_csv('/retweeted_mentions/ret_mentions.csv')
    return ret_mentions

if __name__ == '__main__':
    main()