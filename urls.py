""" Functions for Searching and Retrieving Papers """

from requester import Requester
from bs4 import BeautifulSoup


base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def build_search(search_term, db="db=pubmed", retmax=str(3)):

	search_base = base_url + "esearch.fcgi?"
	search = search_base + db + "&" + "term=" + search_term + "&" + "retmax=" + retmax

	return search


def build_fetch(uid, db="db=pubmed",retmode="retmode=xml"):

	fetch_base = base_url + "efectch.fcgi?"
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


# search = build_search("aging")
# ids = get_ids(search)
# print(ids)

# fetch = build_fetch(ids[0])
# print(fetch)