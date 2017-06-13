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

		self.title = extract(article, 'articletitle', 'str')
		self.authors = _process_authors(extract(article, 'authorlist', 'raw'))
		self.journal = extract(article, 'title', 'str'), extract(article, 'isoabbreviation', 'str')
		self.text = process_text(extract(article, 'abstracttext', 'str'))
		self.year = extract(extract(article, 'datecreated', 'raw'), 'year', 'str')


	def scrape_data(self):

		# Set date of when data was collected
		self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

		fetch_url = build_fetch(self.id)

		article = self.req.get_url(fetch_url)
		article_soup = BeautifulSoup(article.content, 'lxml')
		# print(article_soup)

		self.extract_add_info(article_soup)

		self.req.close()





def init_papers(ids):

	papers = [Paper(id) for id in ids]

	for paper in papers:
		extract_add_info(paper)

	return papers






def crawl():

	links = []
	base_url = "https://www.nih.gov/news-events/news-releases"

	page = Requester()
	page = page.get_url(base_url)
	page_soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer('a', href=True))
	# print(page_soup.prettify())


	for link in page_soup.find_all('a'):
		something = link.get('href')
		if something not in links and '/news-events/news-releases' in something:
			links.append(link.get('href'))

	print(links)




class Press_Release(Base):

	def __init__(self):

		Base.__init__(self)

		self.source = str()  # NIH


	def scrape_data(self):

		self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

		# url = find_urls()
		url = "https://www.nih.gov/news-events/news-releases/pregnancy-diet-high-refined-grains-could-increase-child-obesity-risk-age-7-nih-study-suggests"

		article = self.req.get_url(url)
		pr_soup = BeautifulSoup(article.content, "lxml")

		self.extract_add_info(pr_soup)

		self.req.close()


	def extract_add_info(self, article):

		self.source = article.find("meta", property="og:site_name")
		self.title = extract(article, 'title', 'str')
		self.text = article.find_all("body")
		self.year = article.find("meta", property="article:published_time")
		# self.year = extract(extract(article, 'published_date', 'raw'), 'year', 'str')



	# def find_urls(self, site="https://www.nih.gov/news-events/news-releases"):



""" Necessary functions:
	1) Get the data from a press release: scrape_data() + extract(), just like for papers
	2) Scrape through the NIH website to compile links to all the different press releases """


"""
def extract/add info (or do this in base and use that fxn)
"""







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

	text = text.decode('utf-8')

	# Tokenize input text
	# words = nltk.word_tokenize(text)
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
    authors = extract(author_list, 'author', 'all')

    # Initialize list to return
    out = []

    # Extract data for each author
    for author in authors:
        out.append((extract(author, 'lastname', 'str'), extract(author, 'forename', 'str'),
                    extract(author, 'initials', 'str'), extract(author, 'affiliation', 'str')))

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

