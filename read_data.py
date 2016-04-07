import glob
import os
import csv
import pickle
training_tweets = []
training_tweet_labels = []

testing_pos_tweets = []
testing_pos_labels = []
testing_neg_tweets = []
testing_neg_labels = []
POSITIVE = 1
NEGATIVE = 0


def pickle_data(data, file_path):
	pickle.dump(data, open(os.path.join(os.path.dirname(__file__), file_path), "wb"))


def load_pickle(file_path):
	return pickle.load(open(os.path.join(os.path.dirname(__file__), file_path), "rb"))


def read_csv_training_data(path):
	file_path = os.path.join(os.path.dirname(__file__), path)
	with open(file_path, 'rb') as csvfile:
		filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in filereader:
			sentiment = row[1]
			tweet = row[3]
			training_tweets.append(tweet)
			training_tweet_labels.append(sentiment)
		return training_tweets, training_tweet_labels


def read_csv_testing_data(path, isWordBasedSentiment):
	file_path = os.path.join(os.path.dirname(__file__), path)
	with open(file_path, 'rb') as csvfile:
		filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in filereader:
				sentiment = row[1]
				tweet = row[3]
				if sentiment == str(POSITIVE) or sentiment == '"positive"':
					testing_pos_tweets.append(tweet)
					testing_pos_labels.append(1)
				else:
					testing_neg_tweets.append(tweet)
					testing_neg_labels.append(0)

		return testing_pos_tweets, testing_pos_labels, testing_neg_tweets, testing_neg_labels;

def read_training_data(negative_path, positive_path):
	neg_files = glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), negative_path), '*'))
	pos_files = glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), positive_path), '*'))
	read_neg(neg_files, training_tweets, training_tweet_labels)
	read_pos(pos_files, training_tweets, training_tweet_labels)
	return training_tweets, training_tweet_labels


def read_testing_data(path, isNeg):
	files = glob.glob(os.path.join(os.path.join(os.path.dirname(__file__), path), '*'))
	if isNeg == True:
		read_neg(files, testing_pos_tweets, testing_pos_labels)
		return testing_pos_tweets, testing_pos_labels
	else:
		read_pos(files, testing_neg_tweets, testing_neg_labels)
		return testing_neg_tweets, testing_neg_labels


def read_neg(neg_files, tweets, tweet_labels):
	for negative in neg_files:
		with open(negative, 'r')as file:
			text = file.read()
			text = unicode(text, "utf-8", "ignore")
			tweets.append(text)
			tweet_labels.append(NEGATIVE)


def read_pos(pos_files, tweets, tweet_labels):
	for positive in pos_files:
		with open(positive, 'r')as file:
			text = file.read()
			text = unicode(text, "utf-8", "ignore")
			tweets.append(text)
			tweet_labels.append(POSITIVE)
