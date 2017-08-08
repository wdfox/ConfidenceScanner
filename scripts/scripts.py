'''Functions designed to collect all data starting with a single search term/database pairing'''

import base
import urls
import data
from requester import Requester

import os



def collect_papers(paper_count, search_term, use_hist=False):
    """Collects a given number of papers related to a given term

    Parameters
    ----------
    paper_count : str
        Number of papers to be collected and saved
    search_term : str
        Papers returned will be associated with this term
    use_hist : Bool
        Whether to employ the EUtils use_history feature for large scrapes

    Notes
    -----
    - Decide between a temp file or archive
    """

    req = Requester()

    # Create a location to save the collected papers
    path = data.build_path(data_type='Papers', search_term=search_term)

    # Save a header file with the database info
    # urls.save_db_info(path)

    # Using history
    if use_hist:

        ret_start = 0
        ret_max = 100

        count = int(page_soup.find('count').text)
        web_env = page_soup.find('webenv').text
        query_key = page_soup.find('querykey').text

        while ret_start < count:

            art_url = None# FIGURE THIS OUT
            
            # Scrape and save data for each article into JSON
            data.scrape_paper_data(art_url, path, ret_start)

            # Increment ret_start to get next batch of papers
            ret_start += ret_max

    else:

        # Build search URL
        search = urls.build_search(search_term, retmax=paper_count)
        
        # Get associated IDs
        ids = urls.get_ids(search)

        # Get the fetch URL for papers
        art_url = urls.build_fetch(ids)

        # Scrape and save data for each article into JSON
        data.scrape_paper_data(art_url, path)

    # Clear archived data after a successful scrape
    data.clear_archive()


def collect_prs(pr_count, db_url="https://www.nih.gov/news-events/news-releases"):
    """Collects a given number of press releases related to a given term

    Parameters
    ----------
    pr_count : str
        Number of press releases to be collected and saved
    db_url : str
        Base URL from which to begin the search for individual press release links (preset to NIH db)

    Notes
    -----
    - Currently this function overwrites the existing file every time it runs
    - Implement the whole save path deal as above
    """

    # Retrieve press release URLS
    pr_links = urls.crawl(db_url)

    # Create a list of press release objects to be saved
    prs = []
    for link in pr_links:
        if len(prs) < pr_count:
            prs.append(base.Press_Release(db_url+link))

    # Initialize an index to be used in saving the papers
    i = 0

    # Extract the desired info from each press release and save to JSON
    for ind, pr in enumerate(prs):
        pr.scrape_data()
        outfile = '{:04d}.json'.format(ind)
        data.save(path, outfile, pr)
