"""Functions designed to collect all data starting with a single search term/database pairing"""

import base
import urls
import data

def collect_papers(search_term, paper_count):

    search = urls.build_search(search_term, retmax=paper_count)
    ids = urls.get_ids(search)

    papers = []
    for id in ids:
        papers.append(base.Paper(id))
        # do I have to check whether the paper with a given id is already in the saved data??? Or can I just scrape a new file every time?

    for paper in papers:
        paper.scrape_data()
        data.save('Papers', search_term, paper)




def collect_prs(db_url="https://www.nih.gov/news-events/news-releases", pr_count):

    pr_links = urls.crawl(db_url)

    prs = []
    for link in pr_links:
        if len(prs) <= pr_count:
            prs.append(base.Press_Release(db_url+link))

    for pr in prs:
        pr.scrape_data()
        # DB means database
        data.save('PRs', db_url, pr)
