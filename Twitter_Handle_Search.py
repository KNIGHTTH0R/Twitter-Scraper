import twitter
import time
import json
import os
import datetime


class handle_search:
    def __init__(self):
        self.token = {}
        self.api = twitter.Api

    def get_auth_key(self, token_file_name):
        with open(token_file_name) as f:
            self.token = json.load(f)

    def twitter_auth(self):
        self.api = twitter.Api(consumer_key=self.token['CK'],
                               consumer_secret=self.token['CS'],
                               access_token_key=self.token['TK'],
                               access_token_secret=self.token['TS'],
                               tweet_mode='extended')

    def get_user_timeline(self, user_id):
        result = self.api.GetUserTimeline(user_id=user_id)
        print(result)

    def get_retweets(self, status_id):
        result = self.api.GetRetweets(statusid=status_id)

    def get_tweet_search(self):
        raw_query = 'q=public policy&lang=en&result_type=recent'
        results = self.api.GetSearch(raw_query=raw_query)
        return results


    def get_reply(self, status_id):
        raw_query = 'q=%40GovRicketts&since_id=' + str(status_id)
        results = self.api.GetSearch(raw_query=raw_query)
        related_results = []
        for result in results:
            if result.in_reply_to_status_id==status_id:
                related_results.append(result)
        return related_results




a = handle_search()
a.get_auth_key('Access_Token.json')
a.twitter_auth()
#a.get_user_timeline(user_id=2891165960)
#result = a.get_reply(status_id=1106693546411782144)
results = a.get_tweet_search()


#StatusID = 1106665623281647617

