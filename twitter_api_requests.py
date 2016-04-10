consumer_key = "uhSIdEYDT1FrUbHvZHpADHKwV"
consumer_secret = 'zbxE2mIIcISQpHXPoiAtzoS8ExU0NXhb0DF2HtqKRDaSWMsiTf'
access_token = '568372184-6vq61njUZkn0RcgACBgfdRs6CzkGvkFJR0J7v3vx'
access_token_secret = 'DLc5FgDXSiYLVtplQM0Z01BEsbww9EgcNK4QyQwuyvJHW'

accounts = [
    {
        'consumer_key': "uhSIdEYDT1FrUbHvZHpADHKwV",
        'consumer_secret': 'zbxE2mIIcISQpHXPoiAtzoS8ExU0NXhb0DF2HtqKRDaSWMsiTf',
        'access_token': '568372184-6vq61njUZkn0RcgACBgfdRs6CzkGvkFJR0J7v3vx',
        'access_token_secret': 'DLc5FgDXSiYLVtplQM0Z01BEsbww9EgcNK4QyQwuyvJHW'
    },
    {
        'consumer_key': "gHsPyTHYZs3r391MScDEFJdtS",
        'consumer_secret': 'R57qa4vzUHcba5w9d0SAVtppAvUzlHShSrJ38KDpDQLJ7onDsG',
        'access_token': '719291610987642881-jSqoOhhXlfcudPyBStMhLJVcra8b1Sv',
        'access_token_secret': 'taFU3qzpLXmRIeW2FKjZ01sl8zHsDYl9dJvFl3Z1s4Fon'
    },
    {
        'consumer_key': "mlyk3hLX913j09tlSrw4Jkgxr",
        'consumer_secret': 'OXClWBP6UiF8o1ecGoRybzSIAjZrBchykMYE84UX9aWmVP0k3n',
        'access_token': '719300342115143681-DhPUFXd7YR5biVQBTL0JbXOKQPTo53E',
        'access_token_secret': 'dNzTbpTd5DkFc1xfAMPKne59ZFLFMXEbYI8Iq9MbjjWeE'
    }
]

import tweepy


class TwitterAPI:

    def select_acc(self, number):
        acc = accounts[number]
        auth = tweepy.OAuthHandler(acc["consumer_key"], acc["consumer_secret"])
        auth.set_access_token(acc["access_token"], acc["access_token_secret"])
        self.api = tweepy.API(auth)

    def __init__(self):
        self.cached_trends = []

        self.select_acc(1)

        self.attempts = 0
        self.account_len = len(accounts)

    def search_twitter(self, query='', geo='&geocode=37.781157%2C-122.398720%2C1mi', items=100):
        try:
            return tweepy.Cursor(self.api.search, q=query, geocode=geo, lang='en').items(items)
        except tweepy.TweepError as e:
            print e

            return []

    def find_trending(self, location=23424977):
        try:
            trends1 = self.api.trends_place(location)
            data = trends1[0]
            trends = data['trends']
            names = [trend['name'] for trend in trends]
            self.cached_trends = names
        except tweepy.TweepError:
            print "Usage Cap Exceeded"
        return self.cached_trends
