""" git status
    git add
    git commit -m ""
    git push
    git diff """

'''Classes and functions for collecting, cleaning 
   and storing paper and press release info.'''

import datetime
import string
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import urls
from requester import Requester


class Base(object):
    """Base class for running confidence analysis

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
        self.year = str()

        # Requester object for handling URL objects
        self.req = Requester()

        # Initialize for date that data is collected
        self.date = str()


    def remove_special_characters(self):
        """Deletes words with non ascii_lower characters from self.text

        Notes
        -----
        - Use the scrape_data method first"""

        for word in self.text:
            for letter in word:
                if letter not in string.ascii_lowercase:
                    self.text.remove(word)

    
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




class Paper(Base):
    """Class for collecting and analyzing scientific papers.
    
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
    id : str
        ID number of the paper from PubMed database.
    authors : list of tuple of (str, str, str, str)
        List of authors, as (LastName, FirstName, Initials, Affiliation).
    journal : tuple (str, str)
        Tuple containing the journal's full and abbreviated titles.

    See Also
    --------
    - Attributes of Base class.
    """

    def __init__(self, id):
        """Initializes an object to store paper data.

        Parameters
        ----------
        id : str
            ID number of the paper from PubMed database.
        """

        # Initialize to store all of the basic data
        Base.__init__(self)

        # Set ID attribute to the given PubMed ID and paper DOI
        self.id = id
        self.doi = str()

        # Initialize to store the paper authors and publishing journal
        self.authors = list()
        self.journal = tuple()


    def __dict__(self):
        """Creates a dictionary to store the paper object's attributes."""

        return {
                'id' : self.id,
                'doi' : self.doi,
                'title' : self.title,
                'text' : self.text,
                'authors' : self.authors,
                'journal' : self.journal,
                'year' : self.year,
                'date' : self.date
                }


    def extract_add_info(self, article):
        """Extract information from PubMed paper.

        Parameters
        ----------
        article : bs4.BeautifulSoup object
            Extracted PubMed article.

        NOTES
        -----
        - Possible that papers may be missing one or more of these fields
        """

        # Set attributes to be the extracted info from PubMed article.
        self.doi = article.find('articleid', idtype='doi').text
        # self.title = article.articletitle.text
        self.title = _check_extract(article, 'articletitle')
        self.authors = _process_authors(article.authorlist)
        self.journal = _check_extract(article, 'title'), _check_extract(article, 'isoabbreviation')
        # self.text = _process_paper(article.abstracttext.text)
        # self.text = _process_paper(_check_extract(article, 'abstracttext'))
        self.text = _process_paper(article.find_all('abstracttext'))
        self.year = int(article.datecreated.year.text)

        # Ensure all attributes are of correct type
        self._check_type()


    def _check_type(self):
        """Ensures all attributes are of the correct type."""

        assert isinstance(self.id, str)
        assert isinstance(self.doi, str)
        assert isinstance(self.title, str)
        assert isinstance(self.authors, list)
        assert isinstance(self.journal, tuple)
        assert isinstance(self.text, list)
        assert isinstance(self.year, int)



class Press_Release(Base):
    """Class for collecting and analyzing scientific press releases.

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
    url : str
        URL where the press release is found.
    source : str
        Original organization which published the press release.

    See Also
    --------
    - Attributes of Base class.

    Notes
    -----
    - May be worth looking into other sources of press releases as well
        - E.g. journals, universities, EurekAlert!
    """

    def __init__(self, url):
        """Initializes an instance of a class to hold press release info.

        Parameters
        ----------
        url : str
            URL where the press release is found.
        """

        # Initialize to store all of the basic data
        Base.__init__(self)

        # Initialize URL attribute to the given URL
        self.url = url
        # Initialize to store the organization which published the release
        self.source = str()


    def __dict__(self):
        """Creates a dictionary to store the pr object's attributes."""

        return {
                'url' : self.url,
                'title' : self.title,
                'text' : self.text,
                'source' : self.source,
                'year' : self.year,
                'date' : self.date
                }


    def extract_add_info(self, article):
        """Extract information from press release web page.

        Parameters
        ----------
        article : bs4.BeautifulSoup object
            Extracted press release article.

        NOTES
        -----
        - Possible that prs may be missing one or more of these fields
        - process_pr() function and pr heuristics could be improved
        - May need to change the self.year extraction
        """

        # Set attributes to be the extracted info from press release.
        self.title = article.find('meta', property='og:title')['content']
        self.source = article.find('meta', property='og:site_name')['content']
        self.text = _process_pr(article)
        self.year = int(article.find('meta', property='article:published_time')['content'][0:4])


    def _check_type(self):
        """Ensures all attributes are of the correct type."""

        assert isinstance(self.url, str)
        assert isinstance(self.title, str)
        assert isinstance(self.source, str)
        assert isinstance(self.text, list)
        assert isinstance(self.year, int)





##########################################################################
####################### COMSC - UTILS - DECORATORS #######################
##########################################################################

def CatchNone(func):
    """Decorator function to catch and return None, 
                if given as argument."""

    def wrapper(arg):

        if arg is not None:
            return func(arg)
        else:
            return None

    return wrapper





#########################################################################
################## CON - WORDS - FUNCTIONS (PRIVATE) ####################
#########################################################################

@CatchNone
def _process_paper(abstract_tags):
    """Sets abstract text to lower case, removes stopwords and punctuation.

    Parameters
    ----------
    abstract_tags : ResultSet
        Tags from original article denoting all or part of an abstract

    Returns
    -------
    words_cleaned : list of str
        List of words, after processing.
    """

    # Initialize a variable to store the abstract text
    abstract_text = ''

    # Loop through selected tags, combining all pieces of abstract text
    for tag in abstract_tags:
        abstract_text += tag.get_text()

    # Tokenize input text
    words = nltk.word_tokenize(abstract_text)

    # Remove stop words, and non-alphabetical tokens (punctuation).
    return [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
                                                & word.isalnum())]


@CatchNone
def _process_pr(article):
    """Set pr text to lower case, removes stopwords and punctuation.

    Parameters
    ----------
    article : str
        Text as one long string.

    Returns
    -------
    words_cleaned : list of str
        List of words, after processing.
    
    Notes
    -----
    - This function is just heuristics right now - could be improved.
    """

    text = str()

    tags = article.find_all(name='p', class_=False)
    # print(tags)
    
    for tag in tags:
        tag = tag.get_text()
        # Heuristic for eliminating excess text that is unrelated to the article
        if tag == '###':
            break
        text += tag

    # Tokenize the input text
    words = nltk.word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
    return [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
                                            & word.isalnum())]


@CatchNone
def _process_authors(author_list):
    """Reformats information about paper authors.

    Parameters
    ----------
    author_list : bs4.element.Tag
        AuthorList tag, which contains tags related to author data.

    Returns
    -------
    out : list of tuple of (str, str, str, str)
        List of authors, as (LastName, FirstName, Initials, Affiliation).

    Notes
    -----
    - Current try except could be cleaned up?
    """

    # Pull out all author tags from the input
    authors = author_list.find_all('author')

    # Initialize list to return
    out = []

    # Extract data for each author, checking for missing fields
    for author in authors:
        out.append((_check_extract(author, 'lastname'),
                    _check_extract(author, 'forename'),
                    _check_extract(author, 'initials'),
                    _check_extract(author, 'affiliation')
                    ))

    return out


def _check_extract(tag, label):
    
    try:
        return tag.find(label).text
    except:
        return None
