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
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

try:
    pos_data = twitter_samples.strings('positive_tweets.json')
    neg_data = twitter_samples.strings('negative_tweets.json')
except:
    nltk.download('twitter_samples')
    pos_data = twitter_samples.strings('positive_tweets.json')
    neg_data = twitter_samples.strings('negative_tweets.json')

model_lexicon = []
documents = []

print(pos_data[:10])

# stop_words = set(stopwords.words('english'))
word_filter = ["J", "R", "V"]

for datum in pos_data:
    documents.append((datum, 'pos'))
    words = word_tokenize(datum)
    categorized = nltk.pos_tag(words)
    for word in categorized:
        # if word not in stop_words:
        if word[1][0] in word_filter:
            model_lexicon.append(word[0].lower())

for datum in neg_data:
    documents.append((datum, 'neg'))
    words = word_tokenize(datum)
    categorized = nltk.pos_tag(words)
    for word in categorized:
        # if word not in stop_words:
        if word[1][0] in word_filter:
            model_lexicon.append(word[0].lower())

model_lexicon = nltk.FreqDist(model_lexicon)

pickled_lexicon = open("pickles/lexicon.pickle", "wb")
pickle.dump(model_lexicon, pickled_lexicon)
pickled_lexicon.close()


def discover_features(document):
    words = word_tokenize(document)
    features = {}
    for word in model_lexicon:
        features[word] = (word in words)

    return features


feature_data = [(discover_features(data), sentiment) for (data, sentiment) in documents]

random.shuffle(feature_data)

train_set = feature_data[:9500]
val_set = feature_data[9500:9750]
small_test_test = feature_data[9750:]
test_set = feature_data[9500:10000]

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

print("NB Accuracy:", nltk.classify.accuracy(naive_bayes_classifier, test_set))
print("Multinomial NB Accuracy:", nltk.classify.accuracy(multinomial_nb_classifier, test_set))
print("Bernoulli NB Accuracy:", nltk.classify.accuracy(bernoulli_nb_classifier, test_set))
print("SGDC Accuracy:", nltk.classify.accuracy(sgdc_classifier, test_set))
print("SVC Accuracy:", nltk.classify.accuracy(svc_classifier, test_set))
print("Linear SVC Accuracy:", nltk.classify.accuracy(linear_svc_classifier, test_set))
print("NU SVC Accuracy:", nltk.classify.accuracy(nu_svc_classifier, test_set))

import itertools
from scipy import stats as s

class VoteSystem(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers[0]

    def classify(self, featureset):
        votes = []
        for cs in self._classifiers:
            vote = cs.classify(featureset)
            votes.append(vote)
        return s.mode(votes)[0]

classifiers = [naive_bayes_classifier, multinomial_nb_classifier, bernoulli_nb_classifier, sgdc_classifier, svc_classifier, linear_svc_classifier, nu_svc_classifier]
names = ["Naive Bayes", "Multinomial Naive Bayes", "Bernoulli Naive Bayes", "SGD Clasifier", "Support Vector Classifier", "Linear Support Vector Classifier", "NU Support Vector Classifier"]

for i in range(2,8):
    combo = list(itertools.combinations(names, i))
    print("Pick {} classifiers:".format(i))
    for j,c in enumerate(combo):
        statement = "\tVoting Classifier {"
        cs = []
        for x in c:
            statement = statement+x+", "
            cs.append(classifiers[names.index(x)])
        vs = VoteSystem(cs)
        accuracy = nltk.classify.accuracy(vs, val_set)[0]
        statement = statement[:-2]+"} "+"Accuracy: {}".format(accuracy)
        print(statement)
    print()
