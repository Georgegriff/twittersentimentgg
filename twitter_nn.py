import read_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import numpy as np
from ffnet import ffnet, tmlgraph

stop_words = ['a','the','and', 'of', 'or', 'then', 'an']
pattern = '(?u)\\b[A-Za-z]{3,}'
tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words=stop_words,token_pattern=pattern,ngram_range=(1,3))
#read the training_data data
training_tweets, training_labels = read_data.read_training_data("./training_data/negative", "./training_data/positive")

tfidf.fit(training_tweets)
features = tfidf.get_feature_names()
number_of_features = len(features)

input_data = np.zeros((len(training_tweets), number_of_features))


for j,tweet in enumerate(training_tweets):
	input_data[j,:] =  tfidf.transform([tweet]).toarray()[0]


#Create Neural Network
hidden_nodes = number_of_features
connections = tmlgraph((number_of_features, hidden_nodes, 1))
nnet = ffnet(connections)

#train the network
nnet.train_tnc(training_tweets, training_labels, maxfun = 5000, messages=1)
output, regression = nnet.test(training_tweets, training_labels, iprint = 2)
pos_testing, pos_testing_labels = read_data.read_testing_data("./test_data/positive", False)
neg_testing, neg_testing_labels = read_data.read_testing_data("./test_data/negative", True)



def calculate_accuracy():
	pos_total = pos_testing.__len__()
	total =  pos_total + neg_testing.__len__()
	incorrect_negative = np.flatnonzero(results_negative)
	total_incorrect_neg = incorrect_negative.__len__()

	correct_positive = np.flatnonzero(results_positive)
	total_incorrect_pos = pos_total - correct_positive.__len__()

	total_incorrect = total_incorrect_neg + total_incorrect_pos

	return (float(total - total_incorrect) / float(total)) * 100

print "SVM Accuracy: %s%%" % calculate_accuracy()
