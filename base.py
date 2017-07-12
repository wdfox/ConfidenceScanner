""" git status
    git add
    git commit -m ""
    git push
    git diff """

"""Classes and functions for collecting, cleaning 
   and storing paper and press release info."""

import datetime
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import urls
from requester import Requester



class Base():
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

    

    def analyze(self):
        """Runs confidence analysis on text from paper or press release."""
        pass




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
        List of authors, each as (LastName, FirstName, Initials, Affiliation).
    journal : tuple (str, str)
        Tuple containing both the journal's full title and its abbreviated one.

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

        # Set ID attribute to the given ID
        self.id = id

        # Initialize to store the paper authors and publishing journal
        self.authors = list()
        self.journal = tuple()


    def extract_add_info(self, article):
        """Extract information from PubMed paper.

        Parameters
        ----------
        article : bs4.BeautifulSoup object
            Extracted PubMed article.

        NOTES
        -----
        - May be necessary to consider the possibility of papers missing one or more of these fields...
        """

        # Set attributes to be the extracted info from PubMed article.
        self.title = article.articletitle.text
        self.authors = _process_authors(article.authorlist)
        self.journal = article.title.text, article.isoabbreviation.text
        self.text = process_paper(article.abstracttext.text)
        self.year = int(article.datecreated.year.text)


    def scrape_data(self):
        """Retrieve the paper from PubMed and extract the info."""

        # Set date of when data was collected
        self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # Fetches paper with a given ID from PubMed
        fetch_url = urls.build_fetch(self.id)

        # Use Requester() object to open the paper URL
        article = self.req.get_url(fetch_url)

        # Use BeautifulSoup to get paper into a more convenient format for extraction
        article_soup = BeautifulSoup(article.content, 'lxml')

        self.extract_add_info(article_soup)

        # Close the URL request
        self.req.close()

        # Ensure all attributes are of the correct type
        self._check_type()


    def _check_type(self):
        """Ensures all attributes of a paper object are of the right type."""

        assert isinstance(self.id, str)
        assert isinstance(self.title, str)
        assert isinstance(self.authors, list)
        assert isinstance(self.journal, tuple)
        assert isinstance(self.text, list)
        assert isinstance(self.year, int)

        print('All checks passed!')



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


    def extract_add_info(self, article):
        """Extract information from press release web page.

        Parameters
        ----------
        article : bs4.BeautifulSoup object
            Extracted press release article.

        NOTES
        -----
        - May be necessary to consider the possibility of papers missing one or more of these fields...
        - Maybe look into improving the process_pr() function and underlying heuristics
        - May need to change the self.year extraction
        """

        # Set attributes to be the extracted info from press release.
        self.title = article.title.text
        self.source = article.find('meta', property='og:site_name')['content']
        self.text = process_pr(article)
        self.year = int(article.find('meta', property='article:published_time')['content'][0:4])


    def scrape_data(self):
        """Retrieve the press release and extract the info."""

        # Set the date of when the data was collected
        self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # Use Requester() object to open the paper URL
        article = self.req.get_url(self.url)

        # Use BeautifulSoup to get paper into a more convenient format for extraction
        pr_soup = BeautifulSoup(article.content, "lxml")

        self.extract_add_info(pr_soup)

        # Close the URL request
        self.req.close()

        # Ensure all attributes are of the correct type
        self._check_type()


    def _check_type(self):
        """Ensures all attributes of a press release object are of the right type."""

        assert isinstance(self.url, str)
        assert isinstance(self.title, str)
        assert isinstance(self.source, str)
        assert isinstance(self.text, list)
        assert isinstance(self.year, int)

        print('All checks passed!')





################################################################################################
################################## ERPSC - UTILS - DECORATORS ##################################
################################################################################################

def CatchNone(func):
    """Decorator function to catch and return None, 
                if given as argument."""

    def wrapper(arg):

        if arg is not None:
            return func(arg)
        else:
            return None

    return wrapper





#######################################################################################################
  ############################### CON - WORDS - FUNCTIONS (PRIVATE) #################################
#######################################################################################################

@CatchNone
def process_paper(abstract):
    """Processes abstract text - sets to lower case, and removes stopwords and punctuation.

    Parameters
    ----------
    abstract : str
        Text as one long string.

    Returns
    -------
    words_cleaned : list of str
        List of words, after processing.
    """

    # Tokenize input text
    words = nltk.word_tokenize(abstract)

    # Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
    return [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
                                                & word.isalnum())]


@CatchNone
def process_pr(article):
    """Processes press release text - sets to lower case, and removes stopwords and punctuation.

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
    - This function is largely just heuristics right now - could be improved.
    """

    text = str()

    tags = article.find_all(name='p', class_=False)
    # print(tags)
    
    for tag in tags:
        tag = tag.get_text()
        # Heuristic for eliminating excess text that is unrelated to the articlem -- another possibility is 'Article:'
        if tag[0:9] != 'About the':
            text += tag
        else:
            break

    # Tokenize the input text
    words = nltk.word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
    return [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
                                            & word.isalnum())]


@CatchNone
def _process_authors(author_list):
    """ Reformats information about paper authors.

    Parameters
    ----------
    author_list : bs4.element.Tag
        AuthorList tag, which contains tags related to author data.

    Returns
    -------
    out : list of tuple of (str, str, str, str)
        List of authors, each as (LastName, FirstName, Initials, Affiliation).
    """

    # Pull out all author tags from the input
    authors = author_list.find_all('author')

    # Initialize list to return
    out = []

    # Extract data for each author
    for author in authors:
        out.append((author.find('lastname').text, 
                    author.find('forename').text, 
                    author.find('initials').text, 
                    author.find('affiliation').text))

    return out
