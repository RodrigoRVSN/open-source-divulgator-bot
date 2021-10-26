import os
import tweepy
import pandas as pd
import unittest

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
acess_token = os.getenv('ACCESS_TOKEN')
acess_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

class TestRetweetedMentions(unittest.TestCase):
    def test_get_retweeted_mentions(self):
        ret_mentions = pd.read_csv('retweeted_mentions.csv')
        self.assertEqual(get_retweeted_mentions(), ret_mentions)

   
def get_retweeted_mentions():
    ret_mentions = pd.read_csv('/retweeted_mentions/ret_mentions.csv')
    return ret_mentions