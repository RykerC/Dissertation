from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import itertools
import xml.etree.cElementTree as ET
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC

# def word_split(data):
#     data_new = []
#     for word in data:
#         word_filter = [i.lower() for i in word.split()]
#         data_new.append(word_filter)
#     return data_new
# def word_split_sentiment(data):
#     data_new = []
#     for (word, sentiment) in data:    # the sentiment? Why (word, sentiment)this type?
#         word_filter = [i.lower() for i in word.split()]
#         data_new.append((word_filter, sentiment))
#     return data_new
# def word_feature(words):
#     return dict([(word, True) for word in words])
# # the dict command? Convert the output into a dict?
# stopset = set(stopwords.words('english'))- set(('over', 'under', 'below', 'more', 'most',
#                                                 'no', 'not', 'only', 'such', 'few', 'so',
#                                                 'too', 'very', 'just', 'any', 'once'))
# # What does the set command means?
# def stopword_filtered_word_features(words):
#     return dict([(word, True) for word in words if word not in stopset])
# def bigram_words_features(words, score_fn = BigramAssocMeasures.chi_sq(), n = 200):
#     bigram_finder = BigramCollocationFinder.from_words(words)
#     bigrams = bigram_finder.nbest(score_fn, n)
#     return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])
# # BigramAssocMeasures.chi_sq this command? What does this actually working? what output can we get?
# # the nbest command? score_fn? the total function is aimed to do the features selection?
# def evaluate_classifier(featx):
#     negative_features = [(featx(f), 'negative') for f in word_split(negdata)]
#     positive_features = [(featx(f), 'positive') for f in word_split(posdata)]
# # the command featx(f)? What does this type data mean?

tree = ET.ElementTree(file='Restaurants_Train.xml')
root = tree.getroot()
sentence_list_train = []
for i in xrange(0, len(root)):
    sentence_list_train.append(root[i][0].text)
aspect_dic_train = {}
aspect_list_train = []
aspectcategory_dic_train = {}
aspectcategory_list_train = []
tag = 0
for i in xrange(0, len(root)):
    # for aspect in root[i].iter('aspectTerm'):
    #     aspect_dic_train[tag] = aspect.attrib
    #     tag +=1
    # aspect_list_train.append(aspect_dic_train)
    for aspect in root[i].iter('aspectCategory'):
        aspectcategory_dic_train[tag] = aspect.attrib
        tag +=1
    aspectcategory_list_train.append(aspectcategory_dic_train)
terms_list = []
polarity_list = []
# for x in aspect_list_train:
#     terms_list.append(x['term'])
#     polarity_list.append(x['polarity'])


print aspectcategory_list_train

# print polarity_list

# from sklearn import cross_validation
# features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(terms_list, polarity_list, test_size=0.4, random_state=42)
# from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english', ngram_range=(1, 3))
# features_train = vectorizer.fit_transform(features_train)
# features_test  = vectorizer.transform(features_test)
# # labels_train = vectorizer.fit_transform(labels_train)
# # labels_test  = vectorizer.transform(labels_test)
#
# from sklearn.naive_bayes import GaussianNB
# clf = GaussianNB()
# clf = LinearSVC()
# clf.fit(features_train, labels_train)
# prediction = clf.predict(features_test)
# from sklearn.metrics import accuracy_score
# print accuracy_score(prediction, labels_test)



tree_test = ET.ElementTree(file='Restaurants_Test_Data_PhaseA.xml')
root_test = tree_test.getroot()
sentence_list_test = []
for i in xrange(0, len(root_test)):
    sentence_list_test.append(root_test[i][0].text)


stopwords_free_list = []
stop = set(stopwords.words('english'))
for sent in sentence_list_test:
    words = sent.split()
    non_stop_words = []
    for w in words:
        if w not in stop:
            non_stop_words.append(w)
    stopwords_free_list.append(' '.join(non_stop_words))
# print stopwords_free_list

# vectorizer = sklearn.feature_extraction.text.CounterVectorizer(stopwords = 'english')
# # test = sklearn.cross_validation.
# train_matrix = vectorizer.fit_transform(aspect_list_train)
# test_matrix = vectorizer.transform(sentence_list_test)