'''Functions for Searching and Retrieving Papers'''

import os
import json
from bs4 import BeautifulSoup

from consc.requester import Requester

###################################################################################################
###################################################################################################

# URL for searching the PubMed online database
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

###################################################################################################
###################################################################################################

def build_search(search_term, retmax, use_hist=False, db="db=pubmed", mindate=None, maxdate=None):
    """Build URL to search for papers associated with certain keywords.

    Parameters
    ----------
    search_term : str
        Paper ids found will have association with this search term
    retmax : str
        Number of paper ids to be returned
    use_hist : Bool
        Whether to employ the EUtils use_history feature for large scrapes
    db : str
        Specify the database to search (preset as PubMed)
    min_date : datetime object
        Search only for papers published after this date
    max_date : datetime object
        Search only for papers published before this date

    Returns
    -------
    search : str
        URL to a page containing the specified number of paper IDs associated with a given term

    Notes
    -----
    - Search built according to the PubMed URL API
    """

    # Convert use_hist boolean into str form
    if use_hist:
        use_hist = "&usehistory=y"
    else:
        use_hist = ""

    if mindate and maxdate:
        date = "&datetype=pdat&mindate=" + str(mindate) + "&maxdate=" + str(maxdate)
    else:
        date = ""

    # Join all parts of the URL into a usable search
    search_base = BASE_URL + "esearch.fcgi?"
    search = search_base + db + "&term=" + search_term + date + use_hist + "&retmax=" + retmax

    return search


def build_fetch(ids, use_hist=False, query_key=None, WebEnv=None, retstart=None,
                retmax=None, retmode="&retmode=xml", db="db=pubmed"):
    """Function for finding specific papers given their IDs

    Parameters
    ----------
    ids : list
        ID numbers of the papers to retrieve
    use_hist: Bool
        Whether to use the EUtils feature, use history, for large scrapes
    query_key : str
        Key for a previous search call to identify results
    WebEnv : str
        Environment tied to a previous search call
    retstart : int
        Index from which to begin paper collection
    retmax : int
        Number of papers to be collected (per fetch call)
    retmode : str
        Format the paper is returned in (preset as XML)
    db : str
        Specify the database to search (preset as PubMed)

    Returns
    -------
    fetch : str
        URL to a page containing the paper in its specified (XML) format

    Notes
    -----
    - Fetch built according the specifications of the PubMed URL API
    """

    fetch_base = BASE_URL + 'efetch.fcgi?'

    # Using history
    if use_hist:

        # Raise error if user didn't enter enough information to make fetch call
        if query_key is None or WebEnv is None or retstart is None or retmax is None:
            raise Exception('Must specify query_key, WebEnv, retstart, and retmax if using history')

        # Otherwise, build the fetch URL
        else:
            fetch = fetch_base + db + '&query_key=' + query_key + '&WebEnv=' + WebEnv \
            + retmode + '&retstart=' + str(retstart) + '&retmax=' + str(retmax)

    # Using IDs
    elif not use_hist:

        # Check type of IDs that are passed into the function -- must be a list for .join() method to work
        if isinstance(ids, list):

            # Join the list of IDs together, separated by commas
            ids_str = ','.join(ids)

            # Build fetch with list of IDs
            fetch = fetch_base + db + retmode + "&id=" + ids_str

        # Raise error if IDs are not given as a list
        else:
            raise Exception('Please give Ids as a list')

    return fetch


def build_info(db='db=pubmed', retmode='retmode=xml'):
    """Function for finding database info using NCBI's EInfo call

    Parameters
    ----------
    db : str
        Specify the database to search (preset as PubMed)
    retmode : str
        Format the paper is returned in (preset as XML)

    Returns
    -------
    info : str
        URL to a page containing pertinent database info
    """

    # Build the EInfo URL
    info_base = BASE_URL + 'einfo.fcgi?'
    info = info_base + db + '&' + retmode

    return info


def save_db_info(save_location):
    """Saves a header file with the database info for a given scrape

    Parameters
    ----------
    save_location : str
        Path to the save location for a given scrape
    """

    # Initialize a requester object to handle URL calls
    req = Requester()

    # Get the URL for the database EInfo call
    info_url = build_info()
    page = req.get_url(info_url)

    # More convenient form for extraction
    page_soup = BeautifulSoup(page.content, 'lxml')

    # Initialize a dictionary to store relevant info
    db_info = {}

    # Extract info from the webpage
    db_info['dbname'] = page_soup.dbinfo.dbname.text
    db_info['count'] = page_soup.dbinfo.count.text
    db_info['dbbuild'] = page_soup.dbinfo.dbbuild.text
    db_info['lastupdate'] = page_soup.dbinfo.lastupdate.text

    # Store the path to the save location
    save_location = os.path.join(save_location, 'db_info.json')

    # Save the database info header file
    with open(save_location, 'w') as header_file:
        json.dump(db_info, header_file)


def get_ids(search_url):
    """Extract all paper IDs from PubMed search

    Parameters
    ----------
    search_url : str
        URL from build_search() function to a list of IDs associated with a given term

    Returns
    -------
    str_ids : list of str
        List of all paper IDs as strings from the search URL
    """

    # Use requester object to open the search URL
    req = Requester()
    page = req.get_url(search_url)

    # Use BeatifulSoup to convert webpage into a more convenient form for extraction
    page_soup = BeautifulSoup(page.content, "lxml")

    # Get all the ids from the page
    ids = page_soup.find_all("id")

    # Convert IDs to str
    str_ids = ids_to_str(ids)

    return str_ids


def ids_to_str(ids):
    """Extracts IDs and converts them to str

    Parameters
    ----------
    ids : bs4.element.ResultSet
        Object containing all paper ID tags found on the search webpage

    Returns
    -------
    str_ids : list of str
        List of all paper IDs as strings from the search URL

    Notes
    -----
    - Splices from index 4 to index -5 to remove unneccesary parts of the BeautifulSoup 'id' tag
    """

    # Initialize list of the IDs to return
    str_ids = []

    # Convert to string and clean IDs
    for uid in ids:
        uid = str(uid)
        str_ids.append(uid[4:-5])

    return str_ids


def get_use_hist(search_url):
    """Extract all necessary info for a PubMed paper search using history

    Parameters
    ----------
    search_url : str
        URL from build_search() function to a list of IDs associated with a given term

    Returns
    -------
    count, query_key, WebEnv : tuple (str, str, str)
        Tuple containing info necessary to make a fetch call for desired papers
    """

    # Use requester to opent the search url
    req = Requester()
    page = req.get_url(search_url)

    # Use BeatifulSoup to convert webpage into a more convenient form for extraction
    page_soup = BeautifulSoup(page.content, "lxml")

    # Extract the necessary information from the page for use history call
    count = int(page_soup.find('count').text)
    query_key = page_soup.find('querykey').text
    WebEnv = page_soup.find('webenv').text

    return count, query_key, WebEnv

