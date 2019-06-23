import twitter
import time
import json
import os
import datetime


class CountryTrend:
    def __init__(self, country_name):
        self.country = country_name
        self.token = {}
        self.api = twitter.Api
        self.available_country = []
        self.trend = []
        self.trend_list = []
        self.query_list = []
        self.tweet_dict = {}
        self.path = str(datetime.datetime.now())

    def get_auth_key(self, token_file_name):
        with open(token_file_name) as f:
            self.token = json.load(f)

    def twitter_auth(self):
        self.api = twitter.Api(consumer_key=self.token['CK'],
                               consumer_secret=self.token['CS'],
                               access_token_key=self.token['TK'],
                               access_token_secret=self.token['TS'])

    def get_available_country(self, location_file_name):
        with open(location_file_name) as f:
            location = json.load(f)
        for i in location:
            if i['placeType']['name'] == 'Country':
                self.available_country.append(i)

    def get_trend(self):
        if self.country not in [country['name'] for country in self.available_country]:
            raise LookupError('No country available')
        else:
            woe_id = next(item for item in self.available_country if item['name'] == self.country)['woeid']
            self.trend = self.api.GetTrendsWoeid(woe_id)
            self.trend_list = [trend.name for trend in self.trend]
            self.query_list = [trend.query for trend in self.trend]

    def get_tweet(self):
        for i, query in enumerate(self.query_list):
            if i > 50:
                break
            raw_query = 'q=' + query + '&result_type=mixed&count=100'
            result = self.api.GetSearch(raw_query=raw_query)
            print(result)
            self.tweet_dict[self.trend_list[i]] = result
            time.sleep(0.1)

    def save_tweet(self):
        try:
            os.mkdir(self.path)
        except OSError:
            print("Creation of the directory %s failed" % self.path)
            print("Successfully created the directory %s " % self.path)
        for i, (topic, tweets) in enumerate(self.tweet_dict.items()):
            topic_path = self.path + '/' + topic.replace(' ', '_')
            os.mkdir(topic_path)
            with open (topic_path + '/' + '__metadata__', 'w') as f:
                json.dump(self.trend[i]._json, f)
            for tweet in tweets:
                with open(topic_path + '/' + tweet.id_str, 'w') as f:
                    json.dump(tweet._json, f)



US = CountryTrend('United States')
US.get_auth_key('Access_Token.json')
US.get_available_country('Trend_Location.json')
US.twitter_auth()
US.get_trend()
US.get_tweet()
US.save_tweet()