import read_data
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from preprocessing import TweetProcessing

class TwitterBayes:
    def __init__(self):
        self.preprocessing = TweetProcessing()
        try:
            self.c_vect, self.tfidf, self.mnb_classifier = read_data.load_pickle("./bayes_175k.pickle")
        except:
            stop_words = ['a', 'the', 'and', 'of', 'or', 'then', 'an']
            pattern = '(?u)\\b[A-Za-z]{3,}'
            self.c_vect = CountVectorizer(stop_words=stop_words, max_df=0.5, token_pattern=pattern, ngram_range=(1, 3))

            # read the training_data data
            #training_tweets, training_labels = read_data.read_training_data("./training_data/negative",
                                                                           # "./training_data/positive")


            training_tweets, training_labels = read_data.read_csv_training_data_two("./train_200000.csv", 175000)
            training_tweets = self.preprocessing.preprocess_tweets(training_tweets)

            training_counts = self.c_vect.fit_transform(training_tweets)
            self.tfidf = TfidfTransformer(sublinear_tf=True)
            train_tf = self.tfidf.fit_transform(training_counts)
            self.mnb_classifier = MultinomialNB()
            self.mnb_classifier.fit(train_tf, training_labels)

            read_data.pickle_data([self.c_vect, self.tfidf, self.mnb_classifier], './bayes_175k.pickle')

    def calculate_accuracy(self):

        pos_testing, pos_testing_labels = read_data.read_testing_data("./test_data/positive", False)
        neg_testing, neg_testing_labels = read_data.read_testing_data("./test_data/negative", True)

        pos_testing = self.preprocessing.preprocess_tweets(pos_testing)
        neg_testing = self.preprocessing.preprocess_tweets(neg_testing)

        # Testing Features
        pos_testing_counts = self.c_vect.transform(pos_testing)
        neg_testing_counts = self.c_vect.transform(neg_testing)
        testing_positive_features = self.tfidf.transform(pos_testing_counts)
        testing_negative_features = self.tfidf.transform(neg_testing_counts)

        # Testing Results
        results_negative = self.mnb_classifier.predict(testing_negative_features)
        results_positive = self.mnb_classifier.predict(testing_positive_features)

        pos_total = pos_testing.__len__()
        total = pos_total + neg_testing.__len__()
        incorrect_negative = np.flatnonzero(results_negative)
        total_incorrect_neg = incorrect_negative.__len__()

        correct_positive = np.flatnonzero(results_positive)
        total_incorrect_pos = pos_total - correct_positive.__len__()

        total_incorrect = total_incorrect_neg + total_incorrect_pos

        return (float(total - total_incorrect) / float(total)) * 100

    def predict(self, tweets):
        counts = self.c_vect.transform(tweets)
        features = self.tfidf.transform(counts)
        return self.mnb_classifier.predict(features)
svm = TwitterBayes()
print svm.calculate_accuracy()