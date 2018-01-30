"""Subjectivity Rating with NLTK."""

from nltk.sentiment.util import demo_subjectivity
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import NaiveBayesClassifier
from sklearn.svm import LinearSVC
from pickle import load

###################################################################################################
###################################################################################################

WEIGHTS_FILE = '/Users/tom/Documents/GitCode/Confidence_Scanner/scripts/sa_subjectivity.pickle'
# WEIGHTS_FILE = '/Users/wdfox/Documents/GitCode/Confidence_Scanner/consc/analysis/sa_subjectivity.pickle'

try:
    with open(WEIGHTS_FILE, 'rb') as pickle_file:
        SENTIM_ANALYZER = load(pickle_file)
except: # LookupError:
    print('Cannot find the sentiment analyzer you want to load.')
    print('Training a new one using NaiveBayesClassifier.')
    SENTIM_ANALYZER = demo_subjectivity(NaiveBayesClassifier.train, True)

###################################################################################################
###################################################################################################

# NOTE: Is this used anywhere?
def train(trainer=SklearnClassifier(LinearSVC()).train):

    # Train on demo data from NLTK (default is an SVM)
    sa = demo_subjectivity(trainer, save_analyzer=True)

    return sa

# def sent_subjectivity(sentence):
#   """
#   Classify a single sentence as subjective or objective using a stored
#   SentimentAnalyzer.

#   :param text: a sentence whose subjectivity has to be classified.
#   """

#   return str(SENTIM_ANALYZER.classify(sentence))


def doc_subjectivity(document):

    subj = 0
    obj = 0

    for sent in document.tokens:

        # Classify a single sentence as subjective or objective
        #  This approach uses 'SentimentAnalyzer'
        sent_subj = str(SENTIM_ANALYZER.classify(sent))

        #sent_subj = sent_subjectivity(sent)

        if sent_subj == 'subj':
            subj += 1
        elif sent_subj == 'obj':
            obj += 1

    doc_subjectivity = subj - obj

    return doc_subjectivity


def folder_subjectivity(docs):

    subjectivities = [doc_subjectivity(doc) for doc in docs]

    return subjectivities

