

import datetime
from bs4 import BeautifulSoup
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

		# Add ID of current article

		self.title = extract(article, 'ArticleTitle', 'str')
		self.authors = _process_authors(extract(article, 'AuthorList', 'raw'))
		self.journal = extract(article, 'Title', 'str'), extract(article, 'ISOAbbreciation', 'str')
		self.text = process_text(extract(article, 'AbstractText', 'str'))
		self.year = extract(extract(article, 'DateCreated', 'raw'), 'Year', 'str')

		# What do I return?


	def scrape_data(self):

		# Set date of when data was collected
		self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

		fetch_url = build_fetch(self.id)

		article = self.req.get_url(fetch_url)
		article_soup = BeautifulSoup(article.content, "lxml")

		cur_art = self.extract_add_info(article_soup)

		self.req.close()






    # def scrape_data(self, search_term):
    	
    # 	search = build_search(search_term)
    	
    # 	ids = get_ids(search)

    # 	for uid in ids:
    # 		fetch = build_fetch(uid)




class Press_Release(Base):

	def __init__(self):

		Base.__init__(self)

		self.source = str()  # NIH


	"""
	def extract/add info (or do this in base and use that fxn)
	"""



#######################################################################################################
  ############################### CON - WORDS - FUNCTIONS (PRIVATE) #################################
#######################################################################################################

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
    authors = extract(author_list, 'Author', 'all')

    # Initialize list to return
    out = []

    # Extract data for each author
    for author in authors:
        out.append((extract(author, 'LastName', 'str'), extract(author, 'ForeName', 'str'),
                    extract(author, 'Initials', 'str'), extract(author, 'Affiliation', 'str')))

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

