import read_data
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import traceback
from sklearn import svm
import numpy as np

stop_words = ['a', 'the', 'and', 'of', 'or', 'then', 'an']
pattern = '(?u)\\b[A-Za-z]{3,}'

try:
	svc_classifier, tfidf = read_data.load_pickle("./large_svm.pickle")
except:
	t4 = time.time()
	# read the training_data data
	print "Fitting Vocab..."
	tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words=stop_words, token_pattern=pattern,
							ngram_range=(1, 3))
	training_tweets, training_labels = read_data.read_csv_training_data("./large_training.csv")
	training_matrix = tfidf.fit_transform(training_tweets)
	svc_classifier = svm.LinearSVC()
	print "Training..."
	svc_classifier.fit(training_matrix, training_labels)
	t5 = time.time()
	read_data.pickle_data([svc_classifier, tfidf], "large_svm.pickle")
	print "SVM Trained In Time: %s" % (t5 - t4)

print "Testing..."
pos_testing, pos_testing_labels, neg_testing, neg_testing_labels = read_data.read_csv_testing_data(
	"./large_testing.csv")

# Testing Features
testing_positive_features = tfidf.transform(pos_testing)
testing_negative_features = tfidf.transform(neg_testing)

# Testing Results
results_negative = svc_classifier.predict(testing_negative_features)
results_positive = svc_classifier.predict(testing_positive_features)


def calculate_accuracy():
	pos_total = pos_testing.__len__()
	total = pos_total + neg_testing.__len__()
	incorrect_negative = np.flatnonzero(results_negative)
	total_incorrect_neg = incorrect_negative.__len__()

	correct_positive = np.flatnonzero(results_positive)
	total_incorrect_pos = pos_total - correct_positive.__len__()

	total_incorrect = total_incorrect_neg + total_incorrect_pos

	return (float(total - total_incorrect) / float(total)) * 100


print "Accuracy: %s %%" % calculate_accuracy()
