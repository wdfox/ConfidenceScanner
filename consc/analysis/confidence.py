"""LIWC Confidence Method"""

import pkg_resources as pkg
from consc.data import load_folder

###################################################################################################
###################################################################################################

def load_corpus_words(file_name):
    """   """

    f_name = 'corpus/' + file_name + '.txt'
    f_path = pkg.resource_filename('consc', f_name)

    corpus_file = open(f_path, 'r')
    corpus_words = corpus_file.read().splitlines()
    corpus_file.close()

    return corpus_words


HIGH_CON_WORDS = load_corpus_words('positive')
LOW_CON_WORDS = load_corpus_words('negative')


def doc_confidence(document, norm=False):
    """   """

    confidence = 0

    for i in document.tokens:
        for j in i:

            for k in HIGH_CON_WORDS:
                if k in j:
                    confidence += 1
                    continue

            for l in LOW_CON_WORDS:
                if l in j:
                    confidence -= 1
                    continue

    if norm:
        # The try is in case of division by zero
        #  This can only happen with an empty document, so set score to 0.
        try:
            confidence = confidence / len(document.words)
        except:
            confidence = 0

    return confidence


def folder_confidence(docs, norm=False, data_type=None, search_term=None):
    """   """

    # docs = load_folder(data_type, search_term)

    confidence = [doc_confidence(doc, norm) for doc in docs]

    return confidence
