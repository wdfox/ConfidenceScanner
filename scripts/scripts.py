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

        retstart = 0
        retmax = 10

        search = urls.build_search(search_term, retmax=paper_count, use_hist=True)

        use_hist_info = urls.get_use_hist(search)

        count = use_hist_info[0]
        query_key = use_hist_info[1]
        WebEnv = use_hist_info[2]

        while retstart < int(paper_count):

            art_url = urls.build_fetch(ids=None, use_hist=True, query_key=query_key, WebEnv=WebEnv, retstart=retstart, retmax=retmax)
            print(art_url)

            # Scrape and save data for each article into JSON
            data.scrape_paper_data(art_url, path, retstart)

            # Increment ret_start to get next batch of papers
            retstart += retmax

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


def collect_prs(pr_count, db_url=None):
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

    # Create a location to save the collected papers
    path = data.build_path(data_type='PRs', search_term=db_url)

    # Retrieve press release URLS
    pr_links = urls.crawl(db_url)

    # Create a list of press release objects to be saved
    prs = []
    for link in pr_links:
        if len(prs) < pr_count:
            prs.append(db_url+link)

    # Initialize an index to be used in saving the papers
    i = 0

    # Extract the desired info from each press release and save to JSON
    for ind, url in enumerate(prs):
        pr = scrape_pr_data(url, path)
        outfile = '{:04d}.json'.format(ind)
        data.save(path, outfile, pr)
