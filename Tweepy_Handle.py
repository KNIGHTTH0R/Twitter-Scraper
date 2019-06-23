import tweepy
import sys
import json


class handle_search:
    def __init__(self):
        self.auth = tweepy.OAuthHandler
        self.api = tweepy.API
        self.auth_key = {}

    def authenticate(self, token_file_name):
        with open(token_file_name) as f:
            self.auth_key = json.load(f)
        self.auth = tweepy.OAuthHandler(self.auth_key['CK'], self.auth_key['CS'])
        self.auth.set_access_token(self.auth_key['TK'], self.auth_key['TS'])
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def get_handle_timeline(self, handle_screen_name):
        tweet_list = []
        for tweet in tweepy.Cursor(self.api.user_timeline, screen_name='realDonaldTrump', timeout=999999, count=100, tweet_mode='extended').items(100):
            tweet_list.append(tweet)
        return tweet_list


    def get_tweet_replies(self, main_tweet):
        replies=[]
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        for tweet in tweepy.Cursor(self.api.search,q='to:' + main_tweet.user.screen_name, since_id=main_tweet.id, result_type='recent', tweet_mode='extended').items(500):
            assert isinstance(tweet, object)
            if hasattr(tweet, 'in_reply_to_status_id_str') and (
                    tweet.in_reply_to_status_id_str == main_tweet.id_str):
                replies.append(tweet.full_text)

        print("Tweet :",main_tweet.full_text.translate(non_bmp_map))
        for elements in replies:
            print("Replies :",elements)
        return replies


a = handle_search()
a.authenticate(token_file_name='Access_Token.json')
potus = a.get_handle_timeline(handle_screen_name = 'POTUS')
replies = a.get_tweet_replies(potus[0])
