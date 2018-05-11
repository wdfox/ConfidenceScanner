"""Classes and functions for collecting, cleaning and storing paper and press release info."""

import string

import nltk
from nltk.corpus import stopwords

from consc.requester import Requester

###################################################################################################
###################################################################################################

STOPWORDS_SET = set(stopwords.words('english'))

class Base(object):
    """Base class for running confidence analysis.

    Attributes
    ----------
    title : str
        Title of the paper or press release.
    text : str
        Text in the body of the press release or paper.
    year : str
        Year of publication.
    date : str
        Date that the paper or press release was collected.
    """

    def __init__(self):
        """Initializes an instance of the base class."""

        # Initialize to store basic data pulled from papers/press releases
        self.title = str()
        self.text = str()
        self.date = str()

        self.sentences = list()
        self.tokens = list()
        self.words = list()


    def as_dict(self):
        """Returns a dictionary that stores the base object's attributes."""

        return {
            'title' : self.title,
            'text' : self.text,
            'date' : self.date
        }


    def remove_special_characters(self):
        """Deletes words with non ascii_lower characters from self.text

        Notes
        -----
        - Use the scrape_data method first.
        """

        for word in self.words:
            for letter in word:
                if letter not in string.ascii_lowercase:
                    self.words.remove(word)


    def tokenize(self):
        """Tokenize the full text into sentences."""

        self.sentences = nltk.sent_tokenize(self.text)

        self.tokens = [[word.lower() for word in nltk.word_tokenize(sentence) \
            if ((not word.lower() in STOPWORDS_SET) and word.isalpha())] for sentence in self.sentences]

