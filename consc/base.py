"""Classes and functions for collecting, cleaning and storing paper and press release info."""

import string

import nltk
from nltk.corpus import stopwords

from consc.requester import Requester

###################################################################################################
###################################################################################################

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
    req : Requester()
        Object for handling URL requests.
    date : str
        Date that the paper or press release was collected.
    """

    def __init__(self):
        """Initializes an instance of the base class."""

        # Initialize the lists of confidence terms used
        # self.high_confidence = list()
        # self.low_confidence = list()

        # Initialize to store basic data pulled from papers/press releases
        self.title = str()
        self.text = str()
        self.sentences = list()
        self.words = list()
        self.year = str()

        # Requester object for handling URL objects
        self.req = Requester()

        # Initialize for date that data is collected
        self.date = str()


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


    def tokenize_sentence(self):
        """Tokenize the full text into sentences."""

        self.sentences = nltk.sent_tokenize(self.text)


    def tokenize_words(self):
        """Tokenize the full text into words - removes stopwords, punctuation, and sets as lowercase."""

        # Tokenize the input text
        words = nltk.word_tokenize(self.text)

        # Remove stop words, and non-alphabetical tokens (punctuation).
        self.words = [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
                                                        & word.isalnum())]


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
