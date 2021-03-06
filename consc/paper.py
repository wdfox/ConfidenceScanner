"""Object for storing and working with Paper documents."""

from consc.base import Base
from consc.utils import CatchNone, check_extract

###################################################################################################
###################################################################################################

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
    doi : str
        DOI of the paper (if exists)
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


    def as_dict(self):
        """Return a dictionary to store the paper object's attributes."""

        base_dict = super().as_dict()
        base_dict.update({
            'id' : self.id,
            'doi' : self.doi,
            'authors' : self.authors,
            'journal' : self.journal,
            })

        return base_dict


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
        self.title = check_extract(article, 'articletitle')
        self.authors = _process_authors(article.authorlist)
        self.journal = check_extract(article, 'title'), check_extract(article, 'isoabbreviation')
        self.doi = _process_doi(article.find('articleid', idtype='doi'))
        self.date = _process_date(article.find('articledate'))
        self.text = _process_paper(article.find_all('abstracttext'))

        # Ensure all attributes are of correct type
        self._check_type()


    def _check_type(self):
        """Ensures all attributes are of the correct type."""

        assert isinstance(self.id, str)
        # assert isinstance(self.doi, str)
        assert isinstance(self.title, str)
        # assert isinstance(self.authors, list)
        assert isinstance(self.journal, tuple)
        # assert isinstance(self.text, list)
        # assert isinstance(self.year, int)

###################################################################################################
###################################################################################################

@CatchNone
def _process_doi(tag):

    return tag.text

@CatchNone
def _process_date(tag):
    """Process date."""

    return str(tag.year.get_text()) + '-' + str(tag.month.get_text()) + '-' + str(tag.day.get_text())

@CatchNone
def _process_paper(abstract_tags):
    """Sets abstract text to lower case, removes stopwords and punctuation.

    Parameters
    ----------
    abstract_tags : ResultSet
        Tags from original article denoting all or part of an abstract

    Returns
    -------
    text : str
        Words, after processing all tags.
    """

    # Initialize a variable to store the abstract text
    abstract_text = ''

    # Loop through selected tags, combining all pieces of abstract text
    for tag in abstract_tags:
        abstract_text += tag.get_text()

    text = abstract_text

    return text


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
    """

    # Pull out all author tags from the input
    authors = author_list.find_all('author')

    # Initialize list to return
    out = []

    # Extract data for each author, checking for missing fields
    for author in authors:
        out.append((check_extract(author, 'lastname'),
                    check_extract(author, 'forename'),
                    check_extract(author, 'initials'),
                    check_extract(author, 'affiliation')
                    ))

    return out
