consumer_key = "uhSIdEYDT1FrUbHvZHpADHKwV"
consumer_secret = 'zbxE2mIIcISQpHXPoiAtzoS8ExU0NXhb0DF2HtqKRDaSWMsiTf'
access_token = '568372184-6vq61njUZkn0RcgACBgfdRs6CzkGvkFJR0J7v3vx'
access_token_secret = 'DLc5FgDXSiYLVtplQM0Z01BEsbww9EgcNK4QyQwuyvJHW'
import tweepy


class TwitterAPI:


    def __init__(self):
        self.cached_trends = []
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def search_twitter(self, query='',  items=100):
            try:
                return tweepy.Cursor(self.api.search, q=query, lang='en').items(items)
            except tweepy.TweepError as e:
                print e
                return []

    def find_trending(self):
        try:
            trends1 = self.api.trends_place(1)
            data = trends1[0]
            trends = data['trends']
            names = [trend['name'] for trend in trends]
            self.cached_trends = names
        except tweepy.TweepError:
            print "Usage Cap Exceeded"
        return self.cached_trends

