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

pos_data = twitter_samples.strings('positive_tweets.json')
neg_data = twitter_samples.strings('negative_tweets.json')

model_lexicon = []
documents = []

print(pos_data[:10])

# stop_words = set(stopwords.words('english'))
word_filter = ["J", "R", "v"]

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
test_set = feature_data[9500:10000]

print("Training Naive Bayes...")
classifier = nltk.NaiveBayesClassifier.train(train_set)
curr_file = open("pickles/naive_bayes_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))

classifier = SklearnClassifier(MultinomialNB())
print("Training Multinomial Naive Bayes...")
classifier.train(train_set)
curr_file = open("pickles/multinomial_nb_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))

classifier = SklearnClassifier(BernoulliNB())
print("Training Bernoulli Naive Bayes...")
classifier.train(train_set)
curr_file = open("pickles/bernoulli_nb_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))

classifier = SklearnClassifier(SGDClassifier())
print("Training SGDC...")
classifier.train(train_set)
curr_file = open("pickles/sgdc_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))

classifier = SklearnClassifier(SVC())
print("Training SVC...")
classifier.train(train_set)
curr_file = open("pickles/svc_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))

classifier = SklearnClassifier(LinearSVC())
print("Training Linear SVC...")
classifier.train(train_set)
curr_file = open("pickles/linear_svc_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))

classifier = SklearnClassifier(NuSVC())
print("Training Nu SVC...")
classifier.train(train_set)
curr_file = open("pickles/nu_svc_twitter.pickle", "wb")
pickle.dump(classifier, curr_file)
curr_file.close()
print("Accuracy:", nltk.classify.accuracy(classifier, test_set))
