"""  """

from consc.base import Base
from consc.utils import CatchNone

###################################################################################################
###################################################################################################

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
            #'sentences' : self.sentences,
            #'words' : self.words,
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
        #self.year = int(article.find('meta', property='article:published_time')['content'][0:4])
        self.text = _process_pr(article)
        #self.text, self.sentences, self.words = _process_pr(article)


    def _check_type(self):
        """Ensures all attributes are of the correct type."""

        assert isinstance(self.url, str)
        assert isinstance(self.title, str)
        assert isinstance(self.source, str)
        # assert isinstance(self.text, list)
        # assert isinstance(self.year, int)

###################################################################################################
###################################################################################################

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

    for tag in tags:

        tag = tag.get_text()

        # Heuristic for eliminating excess text that is unrelated to the article
        if tag == '###':
            break

        text += tag

    # Tokenize the text into sentences
    #sentences = nltk.sent_tokenize(text)

    # Tokenize the input text
    # words = nltk.word_tokenize(text)

    # # Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
    # words = [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
    #                                         & word.isalnum())]

    return text#, sentences, words
