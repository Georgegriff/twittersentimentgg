import tweepy
from twitter_svm import TwitterSVM
from flask import Response
import urllib

svm = TwitterSVM()


class TwitterAPI:
    def select_acc(self, number):
        acc = self.accounts[number]
        auth = tweepy.OAuthHandler(acc["consumer_key"], acc["consumer_secret"])
        auth.set_access_token(acc["access_token"], acc["access_token_secret"])
        self.api = tweepy.API(auth)

    def __init__(self):
        self.cached_trends = {}

        self.accounts = [
            {
                'consumer_key': "uhSIdEYDT1FrUbHvZHpADHKwV",
                'consumer_secret': 'zbxE2mIIcISQpHXPoiAtzoS8ExU0NXhb0DF2HtqKRDaSWMsiTf',
                'access_token': '568372184-6vq61njUZkn0RcgACBgfdRs6CzkGvkFJR0J7v3vx',
                'access_token_secret': 'DLc5FgDXSiYLVtplQM0Z01BEsbww9EgcNK4QyQwuyvJHW',
            },
            {
                'consumer_key': "gHsPyTHYZs3r391MScDEFJdtS",
                'consumer_secret': 'R57qa4vzUHcba5w9d0SAVtppAvUzlHShSrJ38KDpDQLJ7onDsG',
                'access_token': '719291610987642881-jSqoOhhXlfcudPyBStMhLJVcra8b1Sv',
                'access_token_secret': 'taFU3qzpLXmRIeW2FKjZ01sl8zHsDYl9dJvFl3Z1s4Fon',
            },
            {
                'consumer_key': "mlyk3hLX913j09tlSrw4Jkgxr",
                'consumer_secret': 'OXClWBP6UiF8o1ecGoRybzSIAjZrBchykMYE84UX9aWmVP0k3n',
                'access_token': '719300342115143681-DhPUFXd7YR5biVQBTL0JbXOKQPTo53E',
                'access_token_secret': 'dNzTbpTd5DkFc1xfAMPKne59ZFLFMXEbYI8Iq9MbjjWeE',
            },
            {
                'consumer_key': "6yOblxv82jUfKiWJzRVWJE3K9",
                'consumer_secret': 'fNUYmD2j0Di6XDJmQXOlaFYbakPPKHVwMNbKbCyywQQYnSgzAr',
                'access_token': '719615862223826944-sP0vIwuWkLCEhq19KsV7a0BxUz1Xz31',
                'access_token_secret': 'yPEhpfg0j77ZUfeo34PrmUAMomftkLzZjHAkyRu5qo3qR',
            }
        ]
        self.account_len = len(self.accounts)

        self.select_acc(2)

        self.current_acc = 0

        self.fail_count = 0

    def place_search(self, query, place):
        return "%s place:%s" % (query, place)

    def perform_search(self, max_id, query, geo, items):
        tweet_list = []
        try:
            if max_id <= 0:
                tweet_list = self.api.search(q=query, geocode=geo, lang='en', count=items)
            else:
                tweet_list = self.api.search(q=query, geocode=geo, lang='en', count=items,
                                             max_id=str(max_id - 1))
        except tweepy.TweepError as e:
            print e
            if self.fail_count < self.account_len:
                print "Switching Accounts..."
                self.fail_count += 1
                if self.current_acc == self.account_len - 1:
                    self.current_acc = 0
                else:
                    self.current_acc += 1
                self.select_acc(self.current_acc)
                self.perform_search(max_id, query, geo, items)
            else:
                print "Out of Accounts..."
                self.fail_count = 0
                tweet_list = []
        return tweet_list

    def search_twitter(self, query='', geo='&geocode=37.781157%2C-122.398720%2C1mi', code='',
                       items=100, max_tweets=100):

        def events(code):
            tweet_list = []
            searched_tweets = 0
            max_id = 0
            is_done = False
            while searched_tweets < max_tweets and not (is_done):
                before_size = searched_tweets
                tweet_list = self.perform_search(max_id, query, geo, items)
                if (searched_tweets + len(tweet_list) == before_size):
                    is_done = True
                self.fail_count = 0
                searched_tweets += len(tweet_list)
                # update the last tweet
                if len(tweet_list) > 0:
                    max_id = tweet_list[-1].id

                print "Tweet total: %s" % (searched_tweets)
                for tweet in tweet_list:
                    results = svm.predict([tweet.text])
                    yield '{"data":{"result": %s, "location":"%s" }}' % (results[0], code)
                    yield ','

        return Response(events(code), mimetype='application/json')

    def find_trending(self, location=23424977):
        try:
            trends1 = self.api.trends_place(location)
            data = trends1[0]
            trends = data['trends']
            names = [trend['name'] for trend in trends]
            self.cached_trends[location] = names
        except tweepy.TweepError:
            print "Usage Cap Exceeded"
        if (location in self.cached_trends):
            return self.cached_trends[location]
        else:
            return []

    def lookup_places(self, q):
        try:
            places = self.api.geo_search(query="q", granularity="admin")
            print "%s, %s" % (places[0].id, places[0].full_name)
            return places
        except tweepy.TweepError as e:
            print e
