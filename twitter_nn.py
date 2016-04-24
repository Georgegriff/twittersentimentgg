import read_data
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np
from ffnet import ffnet, tmlgraph, savenet, loadnet
import time

try:
    tfidf = read_data.load_pickle("./nn.pickle")
except:
    stop_words = ['a', 'the', 'and', 'of', 'or', 'then', 'an']
    pattern = '(?u)\\b[A-Za-z]{3,}'

    tfidf = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words=stop_words, token_pattern=pattern,
                            ngram_range=(1, 3))
    # read the training_data data
    training_tweets, training_labels = read_data.read_training_data("./training_data/negative",
                                                                    "./training_data/positive")

    tfidf.fit(training_tweets)


    read_data.pickle_data(tfidf, './nn.pickle')
try:
    nnet = loadnet("trained_nn.network")

except:
    features = tfidf.get_feature_names()
    number_of_features = len(features)
    input_data = np.zeros((len(training_tweets), number_of_features))

    for j, tweet in enumerate(training_tweets):
        input_data[j, :] = tfidf.transform([tweet]).toarray()[0]

    print 'Creating Neural Network...'
    # Create Neural Network

    hidden_nodes = number_of_features / 1000
    print "Hidden Nodes: %s" % (hidden_nodes)
    print "Number of Features: %s" % (number_of_features)
    print 'Creating the neural network. This will take a while...'
    connections = tmlgraph((number_of_features, hidden_nodes, 1))
    nnet = ffnet(connections)
    # train the network
    print 'Starting the training of the neural network. This will take a while...'
    t4 = time.time()

    nnet.train_tnc(input_data, training_labels, maxfun=500, messages=1)
    t5 = time.time()
    nn_train_time = t5 - t4

    savenet(nnet, "trained_nn.network")

    output, regression = nnet.test(input_data, training_labels, iprint=2)
    print 'Time it took to train the neural network: ' + str(nn_train_time) + ' seconds.'

pos_testing, pos_testing_labels = read_data.read_testing_data("./test_data/positive", False)
neg_testing, neg_testing_labels = read_data.read_testing_data("./test_data/negative", True)
number_of_features = len(tfidf.get_feature_names())
testing_data = pos_testing + neg_testing
testing_labels = pos_testing_labels + neg_testing_labels
test_data = np.zeros((len(testing_data), number_of_features))
for j, sentence in enumerate(testing_data):
    test_data[j, :] = tfidf.transform([sentence]).toarray()[0]

results = nnet(test_data)


def calculate_accuracy(results):
    print "calculating"
    incorrect_counter = 0
    index = 0
    total = len(results)
    for result in results:
        output = int(round(result))
        print "NN Output: %s, Target: %s, Classification: %s, Tweet: %s " % (
        result, testing_labels[index], output, testing_data[index])
        if testing_labels[index] != output:
            incorrect_counter += 1
        index += 1

    return (float(total - incorrect_counter) / float(total)) * 100


print "NN Accuracy: %s%%" % calculate_accuracy(results)
