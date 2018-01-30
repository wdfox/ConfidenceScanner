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


    def analyze(self):
        """Runs confidence analysis on text from paper or press release.

        Notes
        -----
        - What if we trained an algorithm on papers and prs and then had it try to sort unknown texts into one of the categories and see if it can?
        - Maybe consider not tokenizing by words, but by sentence or phrase as well?
        - Linguistic Inquiry and Work Count (LIWC) -- (http://liwc.wpengine.com)
        - Wordnet (http://wordnet.princeton.edu/), SentiWordnet (http://sentiwordnet.isti.cnr.it/)
        - Pointwise Mutual Information for Information Retrieval? (PMI-IR)
        - Perhaps use SentiStrength for positive/negitive identification
        - Useful powerpoint (https://lct-master.org/files/MullenSentimentCourseSlides.pdf)
        - Word database development paper (https://arxiv.org/pdf/1103.2903.pdf)
        - Use text level (reading/writing level) as a control
        - Consider not tokenizing text, save both ways
        - python textblob library maybe?
        """

        classification = nltk.sentiment.util.demo_liu_hu_lexicon(self.text)
        print(classification)

        subjectivity = nltk.sentiment.util.demo_sent_subjectivity(self.text)
        print(subjectivity)

        VADER = nltk.sentiment.util.demo_vader_instance(self.text)
        print(VADER)
