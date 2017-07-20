'''Functions for Searching and Retrieving Papers'''

from requester import Requester
from bs4 import BeautifulSoup, SoupStrainer


# URL for searching the PubMed online database
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def build_search(search_term, retmax, use_hist=False, db="db=pubmed"):
    """Build URL to search for papers associated with certain keywords.

    Parameters
    ----------
    search_term : str
        Paper ids found will have association with this search term
    retmax : str
        Number of paper ids to be returned
    db : str
        Specify the database to search (preset as PubMed)

    Returns
    -------
    search : str
        URL to a page containing the specified number of paper IDs associated with a given term

    Notes
    -----
    - Search built according to the PubMed URL API
    """
    search_base = base_url + "esearch.fcgi?"
    search = search_base + db + "&" + "term=" + search_term + "&" + "retmax=" + retmax

    return search


def build_fetch(uid, use_hist=False, retmode="retmode=xml", db="db=pubmed"):
    """Function for finding a specific paper given its ID

    Parameters
    ----------
    uid : str
        ID number of the paper to retrieve
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

    fetch_base = base_url + "efetch.fcgi?"
    fetch = fetch_base + db + "&" + retmode + "&" + "id=" + uid

    return fetch


def build_info(db='db=pubmed', retmode='retmode=xml'):
    """Function for finding database info using NCBI's EInfo call"""
    
    info_base = base_url + 'einfo.fcgi?'
    info = info_base + db + '&' + retmode

    return info


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


def use_history():
    """Handles large paper calls with NCBI Use History

    Returns
    -------
    papers : list of Paper objects
        List of paper objects collected in the database search

    Notes
    -----
    - Un-tested, not totally sure if it works yet, must integrate with rest of code as well
    - Not sure whether to use scrape_data() function or extract_add_info()?
    - Also have to finish finding the article url. Figure out how to search with use_hist on
    """

    papers = []

    ret_start = 0
    ret_max = 100

    count = int(page_soup.find('count').text)
    web_env = page_soup.find('webenv').text
    query_key = page_soup.find('querykey').text

    while ret_start < count:

        art_url = # FIGURE THIS OUT
        art_page = self.req.get_url(art_url)
        page_soup = BeautifulSoup(art_page.content, 'lxml')

        # Pull out articles
        articles = page_soup.find_all('PubmedArticle')

        # Loop through articles
        for article in articles:

            # For each article, pull the ID and extract relevant info
            paper = base.Paper(article.find('id'))
            # paper.scrape_data() OR paper.extract_add_info()?

            # Add each paper to the list to be returned
            papers.append(paper)

        # Increment ret_start to get next batch of papers
        ret_start += ret_max

    return(papers)


def crawl(start_url, page_number=0, pr_links=list()):
    """Crawls a press release database compiling links to individual articles

    Parameters
    ----------
    start_url : str
        URL of the main press release page - search for links starts from here
    page_number : int
        Indicates the page to start from (preset to 0) - indexed from 0
    pr_links : list of str
        List of the URLs for individual press releases found in the search

    Returns
    -------
    pr_links : list of str
        List of the URLs for individual press releases found

    Notes
    -----
    - The list pr_links is initialized as an argument of the function so that the recursive call
    adds to the original list rather than create a new list for every page that is searched.
    """

    # Initialize requester object for handling URLs
    req = Requester()

    # Open the page to begin the search
    page = req.get_url(start_url)

    # Use BeatifulSoup to convert webpage into a more convenient form for extraction
    title = BeautifulSoup(page.text, 'lxml').title.text
    # Extract links only from page content
    page_soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer('a', href=True))

    # Variable for storing number of links before a page is searched
    len_before = len(pr_links)

    # Not gonna lie sorting through these links is a bit gimmicky
    # Sort through links, adding only those connected to individual press releases
    for tag in page_soup.find_all('a'):
        link = tag.get('href')
        if link not in pr_links and 'news-releases/' in link and link != '/news-releases/feed.xml':
            pr_links.append(link)

    # Ends the search the first time 0 links are added to the list
    if len_before == len(pr_links):
        print(type(pr_links))
        return(pr_links)

    # Increment the page number and generate the URL of the next page
    page_number += 1
    next_page_url = 'https://www.nih.gov/news-events/news-releases?page=' + str(page_number)

    # Recursive call runs through all PR pages
    if 'The page you’re looking for isn’t available' not in title:
        crawl(next_page_url, page_number, pr_links)



'''
Dictionary for storing NIH Databases and their respective search terms for papers
Top section is for sites that should be easier to navigate, bottom sections are each more difficult
Some subdivisions of the NIH were omitted completely because there were not helpful (no science occuring) or too difficult to navigate
'''

db_terms = {
            # Easiest/Closest to existing code
            'https://www.cancer.gov/news-events': 'cancer',  # Not very many PRs
            'https://www.nia.nih.gov/newsroom/press-releases': 'aging', # Works the same as NIH
            'https://www.niaaa.nih.gov/news-events/news-releases': 'alcohol abuse, alcoholism', # Same as NIH
            'https://www.niaid.nih.gov/news-events/news-releases': 'allergy, infectious diseases', # All on 1 page
            'https://www.drugabuse.gov/news-events/news': 'drug abuse', # Same as NIH
            
            'https://www.ninds.nih.gov/News-Events/News-and-Press-Releases/Press-Releases': 'stroke',

            # Medium difficulty
            'https://nei.nih.gov/news/pressreleases': 'eye?', 
            'https://www.nichd.nih.gov/news/releases/Pages/news.aspx': 'child health, human dev',
            'https://www.niddk.nih.gov/news/Pages/news-releases.aspx': 'diabetes, digestive and kidney disease',

            # These look either hard or not that useful
            'https://www.nimh.nih.gov/news/index.shtml': 'mental health',
            'https://www.niehs.nih.gov/news/newsroom/releases/index.cfm': 'environmental health sciences',
            'https://www.nhlbi.nih.gov/news/press-releases': 'heart, lung, blood', 
            'https://www.genome.gov/10000475/current-news-releases/': 'genome',
            'https://www.niams.nih.gov/News_and_Events/': 'arthritis, skin diseases', 
            'https://www.nibib.nih.gov/news-events/newsroom?news-type=29&health-terms=All&pub-date%5Bvalue%5D%5Byear%5D=': 'bioengineering'
            }



""" Control Flow:

    1) Pick a search term
    2) Get a number of paper ids associated with that term
    3) Loop through ids, cleaning and saving the information from each paper to a new object
    4) Then deal with the data/Analyze
	

    """