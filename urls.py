""" Functions for Searching and Retrieving Papers """

from requester import Requester
from bs4 import BeautifulSoup, SoupStrainer


base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def build_search(search_term, retmax, db="db=pubmed"):

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



def crawl(start_url, page_number=0, pr_links=list()):

    page_links = []
    year_links = []


    req = Requester()
    page = req.get_url(start_url)
    title = BeautifulSoup(page.text, 'lxml').title.text
    page_soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer('a', href=True))


    # Not gonna lie sorting through these links is a bit gimmicky
    for tag in page_soup.find_all('a'):
        link = tag.get('href')
        if link not in pr_links and 'news-releases/' in link and link != '/news-releases/feed.xml':
            pr_links.append(link)

        # elif link not in page_links and 'page' in link:
        #     page_links.append(tag.get('href'))
        # elif link not in year_links and 'news-releases?2' in link:
        #     year_links.append(tag.get('href'))


    page_number += 1
    next_page_url = 'https://www.nih.gov/news-events/news-releases?page=' + str(page_number)


    # Should I use recursion (as I do here) or opt instead for the nested for loops and use a fxn to build all web pages?
    # Recursive call here to run through all PR pages
    if 'The page you’re looking for isn’t available' not in title and page_number < 2:
        crawl(next_page_url, page_number, pr_links)

    return(pr_links)



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


Then analysis:

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