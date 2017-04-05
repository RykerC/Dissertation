import os, sys, json, numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import svm
from pprint import pprint
from sklearn.cross_validation import train_test_split
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn import grid_search
from random import randint
from scipy.sparse import csr_matrix
from scipy.sparse import hstack
from time import time

from LexFeatsProcessor import LoadStemmedLex, GetLexFeats


def SpaceTokenizer (Str):
    return [l.strip().split() for l in Str.split('\n') if l]

def GetYFromStringLabels(Labels):
    Y = []
    for L in Labels:
        L = L.strip()
        if 'positive' == L:
            Y.append(1)
        elif 'negative' == L:
            Y.append(-1)
        elif 'neutral' == L:
            Y.append(0)
        elif 'conflict' == L:
            Y.append(2)
        else:
            Y.append(0)
    return Y

def GetXYVocab (NumpSamples=-1):
    StemmedLexicons = LoadStemmedLex()
    Lines = [l.strip() for l in open ('../Task 4/AllTermFeats.txt').xreadlines()][:NumpSamples]
    Sentences = [''.join(l.strip().split(';')[:-2]) for l in open ('../Task 4/RestAspTermABSA.csv').xreadlines()][:NumpSamples]
    LexFeats = [GetLexFeats(Sent, StemmedLexicons) for Sent in Sentences]
    LexFeats = np.array(LexFeats)
    LexFeats = csr_matrix(LexFeats)
    print 'loaded lexicon features of shape', LexFeats.shape

    Samples, Labels = zip(*[tuple(L.split(';')) for L in Lines])
    Y = GetYFromStringLabels(Labels)
    print 'loaded {} samples'.format(len(Samples))
    print 'Label dist: ', Counter(Y)

    CountVecter = CountVectorizer(lowercase=False, dtype=np.float64, binary=False)#,max_df=0.95)
    X = CountVecter.fit_transform(Samples)
    X = Normalizer().fit_transform(X)
    print 'shape of X matrix before adding lex feats', X.shape
    X = hstack([X,LexFeats])
    print 'shape of X matrix after adding lex feats', X.shape
    Vocab = CountVecter.get_feature_names() + ['HLPos', 'HLNeg', 'HLSum', 'NrcPos', 'NrcNeg', 'NrcSum', 'SubjPos', 'SubjNeg', 'SubjSum']
    return X, Y, Vocab
def Main():
    T0 = time()
    X, Y, Vocab = GetXYVocab()
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=randint(0, 100))
    LinearSVC = svm.LinearSVC
    Params = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
    Classifier = grid_search.GridSearchCV(LinearSVC(), Params, n_jobs=-1, cv=3)
    Classifier.fit(X_train, y_train)
    Predict = Classifier.predict(X_test)
    Acc = accuracy_score(y_true=y_test, y_pred=Predict)
    P = precision_score(y_true=y_test, y_pred=Predict, average='micro')
    R = recall_score(y_true=y_test, y_pred=Predict, average='micro')
    F = f1_score(y_true=y_test, y_pred=Predict, average='micro')
    report = classification_report(y_true=y_test, y_pred=Predict)
    print "Time used: {}s".format(time() - T0)
    print "Best Patameters are:", Classifier.best_params_
    print "Accuracy", Acc
    # print "Precision", P
    # print "Recall", R
    # print "f1_score", F
    print "Report", report
if __name__ == '__main__':
    Main()