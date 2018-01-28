"""Functions designed to collect all data starting with a single search term/database pairing.

Notes
-----
- 'collect_papers' & 'collect_prs' are the public functions that should be used to launch scrapes.
- Other functions are sub-functions that should not be launched independently.
- TODO: This organization uses more requester objects than it needs to. Could be condensed.
"""

import time
import random
import datetime
from bs4 import BeautifulSoup

import consc.urls as urls
import consc.data as data
import consc.crawl as crawl
from consc.requester import Requester
from consc.paper import Paper
from consc.press_release import Press_Release

###################################################################################################
###################################################################################################

def collect_papers(search_term, paper_count, use_hist=False):
    """Collects a given number of papers related to a given term

    Parameters
    ----------
    search_term : str
        Papers returned will be associated with this term
    paper_count : int
        Number of papers to be collected and saved
    use_hist : Bool
        Whether to employ the EUtils use_history feature for large scrapes

    Notes
    -----
    - Decide between a temp file or archive
    """

    # Initialize a Requester object to handle URLs
    req = Requester()

    # Create a location to save the collected papers
    path = data.build_path(data_type='Papers', search_term=search_term)

    # Save a header file with the database info
    urls.save_db_info(path)

    # Using history
    if use_hist:

        # Set the desired starting index and number of papers per fetch
        retstart = 0
        retmax = 10

        # Build a search URL for desired IDs, using history
        search = urls.build_search(search_term, retmax=str(paper_count), use_hist=True)

        # Extract the necessary info from search page to make fetch calls
        use_hist_info = urls.get_use_hist(search)

        # Create variables to store the info for fetch calls using history
        count = use_hist_info[0]
        query_key = use_hist_info[1]
        WebEnv = use_hist_info[2]

        # Loop until desired paper count is reached
        while retstart < int(paper_count):

            # Build a fetch URL with the given parameters
            art_url = urls.build_fetch(ids=None, use_hist=True, query_key=query_key,
                                       WebEnv=WebEnv, retstart=retstart, retmax=retmax)

            # Scrape and save data for each article into JSON
            scrape_paper_data(art_url, path, retstart)

            # Increment retstart to get next batch of papers
            retstart += retmax

    else:

        # Build search URL
        search = urls.build_search(search_term, retmax=str(paper_count))

        # Get associated IDs
        ids = urls.get_ids(search)

        # Get the fetch URL for papers
        art_url = urls.build_fetch(ids)

        # Scrape and save data for each article into JSON
        scrape_paper_data(art_url, path)

    # NOTE: do we have to do this?
    # Clear archived data after a successful scrape
    #data.clear_archive()


def collect_prs(search_term, start_date, end_date, pr_count=500):
    """Collects a given number of press releases related to a given term

    Parameters
    ----------
    search_term : str
        Term to search for.
    start_date : datetime.date
        Start date for PRs to be collected.
    end_date : datetime.date
        End date for PRs to be collected.
    pr_count : int
        Number of press releases to be collected and saved

    Notes
    -----
    - Currently this function overwrites the existing file every time it runs
    - Implement the whole save path deal as above
    """

    # Initialize the base URL for EurekAlert press releases
    db_url = 'http://www.eurekalert.org/'

    # Initialize a date to begin the scrape from
    scrape_start_date = start_date

    # Get papers from a specific week of dates
    while scrape_start_date < end_date:

        # End date for each batch is one week past the start date
        scrape_end_date = scrape_start_date.replace(day=scrape_start_date.day+6)

        # Create a location to save the collected papers
        path = data.build_path(data_type='PRs', search_term=search_term, batch=str(scrape_start_date))

        # Retrieve press release URLS
        pr_links = crawl.pr_crawl(pr_count=pr_count, search_term=search_term, start_date=scrape_start_date, end_date=scrape_end_date)

        # Create a list of press release URLs to be saved
        pr_urls = [db_url+link for link in pr_links]

        # Extract the desired info from each press release and save to JSON
        for ind, url in enumerate(pr_urls):
            pr = scrape_pr_data(url, path)
            outfile = '{:04d}.json'.format(ind)
            data.save(path, outfile, pr)

            # Sleep for a variable time to ensure we don't get an IP blocked
            sleep_time = random.uniform(2.0, 3.0)
            time.sleep(sleep_time)

        # Increment the date to collect the following week's press releases
        scrape_start_date = scrape_start_date.replace(day=scrape_start_date.day+7)


def scrape_paper_data(url, path, retstart=0):
    """Retrieve the paper from PubMed and extract the info.

    Parameters
    ----------
    url : str
        Fetch URL for the desired papers
    path : str
        Path to the save location for scraped data
    ret_start : int
        An integer for keeping track of the saving index (so papers don't get saved over others if using history)
    """

    # Initialize Requester object for URL requests
    req = Requester()

    # Use Requester() object to open the paper URL
    art_page = req.get_url(url)

    # Get paper into a more convenient format for info extraction
    page_soup = BeautifulSoup(art_page.content, 'lxml')

    # Pull out articles
    articles = page_soup.find_all('pubmedarticle')

    # Loop through articles
    for ind, article in enumerate(articles):

        # For each article, pull the ID and extract relevant info
        art_id = article.find('articleid', idtype='pubmed').text
        paper = Paper(art_id)
        paper.extract_add_info(article)

        # Ensure all attributes are of the correct type
        paper._check_type()

        # Save paper object to JSON file
        outfile = '{:04d}.json'.format(ind+retstart)
        data.save(path, outfile, paper)

    # Close the URL request
    req.close()


def scrape_pr_data(url, path):
    """Retrieve the press release from Eurekalert and extract the info.

    Parameters
    ----------
    url : str
        Fetch URL for the desired press release
    path : str
        Path to the save location for scraped data
    """

    # Initialize Requester object for URL requests
    req = Requester()

    # Use Requester() to open the press release URL
    art_page = req.get_url(url)

    # Get press release into a more convenient format for info extraction
    page_soup = BeautifulSoup(art_page.content, 'lxml')

    # Initialize a press release object to store the scraped data and extract info
    pr = Press_Release(url)
    pr.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    pr.extract_add_info(page_soup)

    # Close the URL request
    req.close()

    # Ensure all attributes are of the correct type
    #pr._check_type()

    return(pr)
