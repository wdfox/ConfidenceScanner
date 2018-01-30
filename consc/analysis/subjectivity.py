''' Subjectivity Rating with NLTK '''

from nltk.sentiment.util import demo_subjectivity
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from pickle import load


def train(trainer=SklearnClassifier(LinearSVC()).train):

	# Train on demo data from NLTK (default is an SVM)
	sa = demo_subjectivity(trainer, save_analyzer=True)

	return sa


def sent_subjectivity(text):
	"""
	Classify a single sentence as subjective or objective using a stored
	SentimentAnalyzer.

	:param text: a sentence whose subjectivity has to be classified.
	"""
	from nltk.classify import NaiveBayesClassifier
	from nltk.tokenize import regexp

	word_tokenizer = regexp.WhitespaceTokenizer()

	# f_name = '/Users/tom/Documents/GitCode/Confidence_Scanner/scripts/sa_subjectivity.pickle'
	f_name = '/Users/wdfox/Documents/GitCode/Confidence_Scanner/consc/analysis/sa_subjectivity.pickle'

	try:
		with open(f_name, 'rb') as pickle_file:
			sentim_analyzer = load(pickle_file)
	except: # LookupError:
		print('Cannot find the sentiment analyzer you want to load.')
		print('Training a new one using NaiveBayesClassifier.')
		sentim_analyzer = demo_subjectivity(NaiveBayesClassifier.train, True)

	# Tokenize and convert to lower case
	tokenized_text = [word.lower() for word in word_tokenizer.tokenize(text)]

	result = str(sentim_analyzer.classify(tokenized_text))

	return result


def doc_subjectivity(document):

	subj = 0
	obj = 0

	for sent in document.sentences:
		sent_subj = sent_subjectivity(sent)

		if sent_subj == 'subj':
			subj += 1
		elif sent_subj == 'obj':
			obj += 1

	doc_subjectivity = subj - obj

	return doc_subjectivity


def folder_subjectivity(docs):

	# docs = load_folder(data_type, search_term)

	subjectivities = [doc_subjectivity(doc) for doc in docs]

	return subjectivities

