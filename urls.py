""" Functions for Searching and Retrieving Papers """

from requester import Requester
from bs4 import BeautifulSoup


base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def build_search(search_term, db="db=pubmed", retmax=str(3)):

	search_base = base_url + "esearch.fcgi?"
	search = search_base + db + "&" + "term=" + search_term + "&" + "retmax=" + retmax

	return search


def build_fetch(uid, db="db=pubmed",retmode="retmode=xml"):

	fetch_base = base_url + "efetch.fcgi?"
	fetch = fetch_base + db + "&" + retmode + "&" + "id=" + uid

	return fetch


def get_ids(search_url):

	req = Requester()
	page = req.get_url(search_url)

	page_soup = BeautifulSoup(page.content, "lxml")

	# Get all the ids
	ids = page_soup.find_all("id")

	str_ids = ids_to_str(ids)

	return str_ids


def ids_to_str(ids):

	"""Convert to string and then splice from index 4 to index -5"""

	str_ids = []

	for uid in ids:
		uid = str(uid)
		str_ids.append(uid[4:-5])

	return str_ids


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


""" Control Flow:

	1) Pick a search term
	2) Get a number of paper ids associated with that term
	3) Loop through ids, cleaning and saving the information from each paper to a new object
	4) Then deal with the data/Analyze


Then the real fun begins:

	Start with basic sentiment and/or confidence analysis
		(High vs low confidence terms? Linguistics professor?)
	Does it vary by area of research?
	Is the bias even developed in this stage of the process? 
		Perhaps papers themselves are overconfident or only positive findings get published?
	Does it make sense to normalize the confidence by the length of the paper? 
		More text would seem to qualify any sentimentby adding more info. Perhaps it would double the effect of confidence seen
		Could we do it for only papers or only press releases? Might be harder to compare that way
	Compare length--Maybe length has nothing to do with it, just the author
	

	"""