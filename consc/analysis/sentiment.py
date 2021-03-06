"""Sentiment Analysis with Liu Hu Lexicon."""

from consc.data import load_folder
from nltk.corpus import opinion_lexicon
from nltk.sentiment.util import _show_plot
from nltk.sentiment.vader import SentimentIntensityAnalyzer

###################################################################################################
###################################################################################################

POS = set(opinion_lexicon.positive())
NEG = set(opinion_lexicon.negative())


def liu_hu_lexicon(sentence, plot=False):
    """
    Sentiment classification using Liu and Hu opinion lexicon.
    This function simply counts the number of positive, negative and neutral words
    in the sentence and classifies it depending on which polarity is more represented.
    Words that do not appear in the lexicon are considered as neutral.

    :param sentence: a sentence whose polarity has to be classified.
    :param plot: if True, plot a visual representation of the sentence polarity.
    """

    pos_words = 0
    neg_words = 0

    for word in sentence:
        if word in POS:
            pos_words += 1
            #y.append(1) # positive
        elif word in NEG:
            neg_words += 1
            #y.append(-1) # negative
        # else:
            #y.append(0) # neutral

    # if plot:
    #     x = list(range(len(tokenized_sent))) # x axis for the plot
    #     y = []
    #     _show_plot(x, y, x_labels=tokenized_sent, y_labels=['Negative', 'Neutral', 'Positive'])

    polarity = pos_words - neg_words

    return polarity

    # if pos_words > neg_words:
    #   return 'pos', polarity
    # elif pos_words < neg_words:
    #   return polarity
    # elif pos_words == neg_words:
    #   return polarity


def liu_polarity(document, vote=True, normalize=False):
    """

    Parameters
    ----------
    document : str
        The paper or press release to be scored for sentiment
    vote : bool
        If True, each sentence gets an equal 'vote' to determine overall document polarity
    normalize : bool
        Whether to normalize the polarity score by the length of the document (in sentences)
    """

    pos_sentences = 0
    neg_sentences = 0

    doc_polarity = 0

    for sent in document.tokens:
        if vote:
            sent_polarity = liu_hu_lexicon(sent)
            if sent_polarity > 0:
                pos_sentences += 1
            elif sent_polarity < 0:
                neg_sentences += 1
            doc_polarity = pos_sentences - neg_sentences
        else:
            sent_polarity = liu_hu_lexicon(sent)[1]
            doc_polarity += sent_polarity

    if normalize:
        doc_polarity = doc_polarity / float(len(document.sentences))

    return doc_polarity

    # if pos_sentences > neg_sentences:
    #   return 'pos', doc_polarity
    # elif pos_sentences < neg_sentences:
    #   return 'neg', doc_polarity
    # elif pos_sentences == neg_sentences:
    #   return 'neu', doc_polarity


def liu_folder(docs, vote=True, normalize=False, data_type=None, search_term=None):

    # docs = load_folder(data_type, search_term)

    polarities = [liu_polarity(doc, vote, normalize) for doc in docs]

    return polarities


def vader_sentence(sentence):

    sia = SentimentIntensityAnalyzer()

    return sia.polarity_scores(sentence)['compound']


def vader_doc(document):

    polarity = 0

    for sent in document.sentences:
        polarity += vader_sentence(sent)

    return polarity


def vader_folder(docs, data_type=None, search_term=None):

    # docs = load_folder(data_type, search_term)

    polarities = [vader_doc(doc) for doc in docs]

    return polarities

