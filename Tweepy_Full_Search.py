import sys
import json
import time

from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterPager

class full_archive_search:
    def __init__(self, search_term='from:realDonaldTrump lang:en', fromDate='201801010000', toDate='201801150000'):
        self.auth_key = {}
        self.api = TwitterAPI
        self.PRODUCT = 'fullarchive'
        self.LABEL = 'UAT'
        self.search_term = search_term
        self.fromDate = fromDate
        self.toDate = toDate
        self.full_tweet_list = []


    def authenticate(self, token_file_name):
        with open(token_file_name) as f:
            self.auth_key = json.load(f)
        self.api = TwitterAPI(self.auth_key['CK'],
             self.auth_key['CS'],
             self.auth_key['TK'],
             self.auth_key['TS'])

    def get_search(self):
        next = ''
        while True:
            tweets = TwitterPager(self.api,'tweets/search/%s/:%s' % (self.PRODUCT, self.LABEL),
                            {'query': self.search_term,
                             'fromDate': self.fromDate,
                             'toDate': self.toDate})
            print(tweets)
            for tweet in tweets.get_iterator():
                if 'text' in tweet:
                    self.full_tweet_list.append(tweet)





b = full_archive_search()
b.authenticate('Access_Token.json')
b.get_search()