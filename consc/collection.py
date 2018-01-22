'''Functions designed to collect all data starting with a single search term/database pairing'''

import os
import time
import random


import consc.base
import consc.urls
import consc.data
import consc.crawl
from consc.requester import Requester



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
        search = urls.build_search(search_term, retmax=paper_count, use_hist=True)

        # Extract the necessary info from search page to make fetch calls
        use_hist_info = urls.get_use_hist(search)

        # Create variables to store the info for fetch calls using history
        count = use_hist_info[0]
        query_key = use_hist_info[1]
        WebEnv = use_hist_info[2]

        # Loop until desired paper count is reached
        while retstart < int(paper_count):

            # Build a fetch URL with the given parameters
            art_url = urls.build_fetch(ids=None, use_hist=True, query_key=query_key, WebEnv=WebEnv, retstart=retstart, retmax=retmax)

            # Scrape and save data for each article into JSON
            data.scrape_paper_data(art_url, path, retstart)

            # Increment retstart to get next batch of papers
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


def collect_prs(search_term, start_date, end_date, pr_count=500):
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
            pr = data.scrape_pr_data(url, path)
            outfile = '{:04d}.json'.format(ind)
            data.save(path, outfile, pr)

            # Sleep for a variable time to ensure we don't get an IP blocked
            sleep_time = random.uniform(2.0, 3.0)
            time.sleep(sleep_time)

        # Increment the date to collect the following week's press releases
        scrape_start_date = scrape_start_date.replace(day=scrape_start_date.day+7)

