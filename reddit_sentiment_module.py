import nltk
import pickle
import random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.corpus import twitter_samples
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI


class VoteSystem(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, featureset):
        votes = []
        for classifier in self._classifiers:
            vote = classifier.classify(featureset)
            votes.append(vote)
        return mode(votes), votes.count(mode(votes))/len(votes)


curr_file = open("pickles/lexicon.pickle", "rb")
model_lexicon = pickle.load(curr_file)
curr_file.close()


def discover_features(document):
    words = word_tokenize(document)
    features = {}
    for word in model_lexicon:
        features[word] = (word in words)

    return features


curr_file = open("pickles/naive_bayes_twitter.pickle", "rb")
naive_bayes_classifier = pickle.load(curr_file)
curr_file.close()
print("naive bayes classifier loaded")

curr_file = open("pickles/multinomial_nb_twitter.pickle", "rb")
multinomial_nb_classifier = pickle.load(curr_file)
curr_file.close()
print("multinomial naive bayes classifier loaded")

curr_file = open("pickles/bernoulli_nb_twitter.pickle", "rb")
bernoulli_nb_classifier = pickle.load(curr_file)
curr_file.close()
print("bernoulli naive bayes classifier loaded")

curr_file = open("pickles/sgdc_twitter.pickle", "rb")
sgdc_classifier = pickle.load(curr_file)
curr_file.close()
print("sgdc classifier loaded")

curr_file = open("pickles/svc_twitter.pickle", "rb")
svc_classifier = pickle.load(curr_file)
curr_file.close()
print("svc classifier loaded")

curr_file = open("pickles/linear_svc_twitter.pickle", "rb")
linear_svc_classifier = pickle.load(curr_file)
curr_file.close()
print("linear svc classifier loaded")

curr_file = open("pickles/nu_svc_twitter.pickle", "rb")
nu_svc_classifier = pickle.load(curr_file)
curr_file.close()
print("nu svc classifier loaded")

classifier = VoteSystem(
    naive_bayes_classifier,
    multinomial_nb_classifier,
    bernoulli_nb_classifier,
    sgdc_classifier,
    svc_classifier,
    linear_svc_classifier,
    nu_svc_classifier
)


def classify(text):
    features = discover_features(text)
    return classifier.classify(features)
