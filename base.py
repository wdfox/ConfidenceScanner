""" git status
    git add
    git commit -m ""
    git push
    git diff """

import datetime
from bs4 import BeautifulSoup, SoupStrainer
import nltk
from nltk.corpus import stopwords
from urls import *

class Base():
	"""Base class for running confidence analysis

	Attributes
	----------

	"""

	def __init__(self):
		
		# Initialize the lists of confidence terms used
		self.high_confidence = list()
		self.low_confidence = list()

		# Initialize to store basic data pulled from papers/press releases
		self.title = str()
		self.text = str()
		self.year = str()

		# Requester object for handling URL objects
		self.req = Requester()

		# Initialize for date that data is collected
		self.date = str()

	"""
	def set
	def set file
	def check
	def unload
	def get db info
	def analyze
	"""



class Paper(Base):

	def __init__(self, id):

		Base.__init__(self)

		self.id = id

		self.authors = str()
		self.journal = str()


	def extract_add_info(self, article):
		"""Extract information from article web page and add to

		Parameters
		----------
		cur_erp : ERPData() object
			Object to store information for the current ERP term.
		new_id : int
			Paper ID of the new paper.
		art : bs4.element.Tag() object
			Extracted pubmed article.

		NOTES
		-----
		- Data extraction is all in try/except statements in order to
		deal with missing data, since fields may be missing.
		"""


		# Working: title, journal, text, year; Need help: authors
		self.title = article.articletitle.text
		self.authors = _process_authors(article.authorlist)
		# self.authors = _process_authors(extract(article, 'authorlist', 'raw'))
		self.journal = article.title.text, article.isoabbreviation.text
		self.text = process_text(article.abstracttext.text)
		self.year = int(article.datecreated.year.text)


	def scrape_data(self):

		# Set date of when data was collected
		self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

		fetch_url = build_fetch(self.id)

		article = self.req.get_url(fetch_url)
		article_soup = BeautifulSoup(article.content, 'lxml')
		# print(article_soup)

		self.extract_add_info(article_soup)

		self.req.close()

		self.type_check()


	def type_check(self):

		assert isinstance(self.id, str)
		assert isinstance(self.title, str)
		assert isinstance(self.authors, list)
		assert isinstance(self.journal, tuple)
		assert isinstance(self.text, list)
		assert isinstance(self.year, int)

		print('All checks passed!')






def init_papers(ids):

	papers = [Paper(id) for id in ids]

	for paper in papers:
		extract_add_info(paper)

	return papers






class Press_Release(Base):

	def __init__(self, url):

		Base.__init__(self)

		self.url = url
		self.source = str()  # NIH


	def extract_add_info(self, article):

		# Working: title, source, year--year is a bit gimmicky tho...; Need help: text
		self.title = article.title.text
		self.source = article.find('meta', property='og:site_name')['content']
		self.text = article.find_all(name='p', class_=False)
		self.year = int(article.find('meta', property='article:published_time')['content'][0:4])


	def scrape_data(self):

		self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

		# url = "https://www.nih.gov/news-events/news-releases/pregnancy-diet-high-refined-grains-could-increase-child-obesity-risk-age-7-nih-study-suggests"

		article = self.req.get_url(self.url)
		pr_soup = BeautifulSoup(article.content, "lxml")

		# print(pr_soup)

		self.extract_add_info(pr_soup)

		self.req.close()

		self.type_check()


	def type_check(self):

		assert isinstance(self.url, str)
		assert isinstance(self.title, str)
		assert isinstance(self.source, str)
		# assert isinstance(self.text, list)
		assert isinstance(self.year, int)

		print('All checks passed!')





################################################################################################
################################## ERPSC - UTILS - DECORATORS ##################################
################################################################################################

def CatchNone(func):
    """Decorator function to catch and return None, if given as argument."""

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
def process_text(text):
	"""Processes abstract text - sets to lower case, and removes stopwords and punctuation.

	Parameters
	----------
	text : str
		Text as one long string.

	Returns
	-------
	words_cleaned : list of str
		List of words, after processing.
	"""

	# Tokenize input text
	words = nltk.word_tokenize(text)

	# Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
	return [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
												& word.isalnum())]


@CatchNone
def _process_authors(author_list):
    """

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
    authors = authors[0]
	# authors = extract(author_list, 'author', 'all')

    # Initialize list to return
    out = []

    # Extract data for each author
    for author in authors:
    	out.append((authors.find('lastname').text, authors.find('forename').text, authors.find('initials').text, authors.find('affiliation').text))
        # out.append((extract(author, 'lastname', 'str'), extract(author, 'forename', 'str'),
         #            extract(author, 'initials', 'str'), extract(author, 'affiliation', 'str')))

    return out

















def extract(dat, tag, how):
    """Extract data from HTML tag.

    Parameters
    ----------
    dat : bs4.element.Tag
        HTML data to pull specific tag out of.
    tag : str
        Label of the tag to extract.
    how : {'raw', 'all' , 'txt', 'str'}
        Method to extract the data.
            raw - extract an embedded tag
            all - extract all embedded tags
            txt - extract text as unicode
            str - extract text and convert to string

    Returns
    -------
    {bs4.element.Tag, bs4.element.ResultSet, unicode, str, None}
        Requested data from the tag. Returns None is requested tag is unavailable.
    """

    # Use try to be robust to missing tag
    try:
        if how is 'raw':
            return dat.find(tag)
        elif how is 'txt':
            return dat.find(tag).text
        elif how is 'str':
            return dat.find(tag).text.encode('ascii', 'ignore')
        elif how is 'all':
            return dat.findAll(tag)

    except AttributeError:
        return None

