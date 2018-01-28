"""Object for storing and working with Press Release documents."""

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

        # Add PR specific data attributes
        self.institution = str()
        self.description = str()
        self.keywords = list()
        self.funder = str()
        self.journal = str()
        self.meeting = str()
        self.region = str()

        self.source_link = str()
        self.article_link = str()


    def as_dict(self):
        """Returns a dictionary that stores the pr object's attributes."""

        base_dict = super().as_dict()
        base_dict.update({
            'url' : self.url,
            'institution' : self.institution,
            'description' : self.description,
            'keywords' : self.keywords,
            'funder' : self.funder,
            'journal' : self.journal,
            'meeting' : self.meeting,
            'region' : self.region,
            'source_link' : self.source_link,
            'article_link' : self.article_link
            })

        return base_dict


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
        self.title = _process_title(article.find('title'))
        self.institution = _get_content(article.find('meta', {'name':'institution'}))
        self.description = _get_content(article.find('meta', {'name':'description'}))
        self.date = _get_content(article.find('meta', {'name':'date'}))
        self.funder = _get_content(article.find('meta', {'name':'funder'}))
        self.journal = _get_content(article.find('meta', {'name':'journal'}))
        self.meeting = _get_content(article.find('meta', {'name':'meeting'}))
        self.region = _get_content(article.find('meta', {'name':'region'}))
        self.keywords = _process_keywords(_get_content(article.find('meta', {'name':'keywords'})))
        self.text = _process_pr_text(article)
        self.source_link, self.article_link = _find_links(article.find_all('h4'))


    def _check_type(self):
        """Ensures all attributes are of the correct type."""

        assert isinstance(self.url, str)
        assert isinstance(self.title, str)
        assert isinstance(self.source, str)
        # assert isinstance(self.text, list)
        # assert isinstance(self.year, int)

###################################################################################################
###################################################################################################

def _find_links(tags):
    """Search for source & article links, given a list of h4 tags."""

    source_link = None
    article_link = None

    for tag in tags:

        if 'Original Source' in tag:
            source_link = tag.find_next('a')['href']

        if 'Related Journal Article' in tag:
            article_link = tag.find_next('a')['href']

    return source_link, article_link

@CatchNone
def _process_title(title):
    """Process an extracted title."""

    return title.get_text().split('|')[0][:-1]

@CatchNone
def _get_content(tag):
    """Return the content of a provided tag."""

    return tag['content']

@CatchNone
def _process_keywords(kws):
    """Process a string list of keywords."""

    return kws.split(',')

@CatchNone
def _process_pr_text(article):
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

        # Heuristic to ignore text section that we don't want
        #  Drops any with a bold section, including featured meeting, and image descriptions
        #     Note: doesn't all image descriptions, depending on organization - needs checking.
        if tag.find('strong'):
            continue

        tag = tag.get_text()

        # Heuristic for eliminating excess text that is unrelated to the article
        if tag == '###':
            break

        text += tag

    return text
