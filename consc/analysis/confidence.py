''' LIWC Confidence Method '''

high_con_file = open('../corpus/positive.txt', 'r')
high_con_words = high_con_file.read().splitlines()

low_con_file = open('../corpus/negative.txt', 'r')
low_con_words = low_con_file.read().splitlines()

def doc_confidence(document):

	confidence = 0

	for i in document.words:

		for j in high_con_words:
			if j in i:
				confidence += 1

		for k in low_con_words:
			if k in i:
				confidence -= 1

	return confidence


def folder_confidence(data_type, search_term):

	docs = load_folder(data_type, search_term)

	confidence = [doc_confidence(doc) for doc in docs]

	return confidence
