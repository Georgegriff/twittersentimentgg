import re
import os
import csv
class TweetProcessing:

    def __init__(self):

        self.emoticons = {}
        self.slang = {}
        self.setup_emoticons()
        self.setup_slang()
        return

    def preprocess_tweets(self, tweets):
        output = []
        for tweet in tweets:
            output.append(self.preprocess_tweet(tweet))
        return output

    def preprocess_tweet(self, tweet):
        return self.remove_apost(self.replace_slang(self.replace_emoticons(self.remove_username(self.remove_hash_tags(self.remove_URLS(tweet)))))).replace("  ", " ")


    def remove_hash_tags(self, tweet):
        return tweet.replace("#", "")


    def remove_URLS(self, tweet):
        return re.sub(r"www\S+", "", re.sub(r"http\S+", "", tweet))

    def remove_apost(self, tweet):
        return tweet.replace("'", "")

    def replace_emoticons(self, tweet):
        tokens = tweet.split(" ")
        output = ""
        counter = 0
        for token in tokens:
            if counter == 0:
                space = ""
            else:
                space = " "
            if token in self.emoticons:
                output += space + self.emoticons[token]
            else:
                output += space + token
            counter += 1
        return output

    def replace_slang(self, tweet):
        tokens = tweet.split(" ")
        output = ""

        counter = 0
        for token in tokens:
            token = self.remove_repeating(token)
            if counter == 0:
                space = ""
            else:
                space = " "
            if token in self.slang:
                output += space + self.slang[token]
            else:
                output += space + token
            counter+=1
        return output

    def remove_repeating(self, word):
        previous = ""
        count = 0
        output = ""
        for character in word:
            if character != previous:
                previous = character
                count = 0
                output += character
            else:
                if count < 1:
                    output += character
                    count += 1
        return output


    def remove_username(self, tweet):
        return re.sub(r"@\S+", "", re.sub(r"RT @\S+", "", tweet))


    def setup_emoticons(self):
        file_path = os.path.join(os.path.dirname(__file__), "emoticons.txt")
        with open(file_path, 'rb') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in filereader:
                try:
                    meaning = row[0]
                    emoticon = row[1]
                except:
                    print row
                self.emoticons[emoticon] = meaning

    def setup_slang(self):
        file_path = os.path.join(os.path.dirname(__file__), "slang.txt")
        counter = 1
        with open(file_path, 'rb') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in filereader:
                try:
                    slang = row[0]
                    translation = row[1]
                except:
                    print row
                    print counter
                counter+=1
                self.slang[slang] = translation
