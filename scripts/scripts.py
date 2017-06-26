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
        # would it work to do paper.scrape_data() right here?
        # do I have to check whether the paper with a given id is already in the saved data??? Or can I just scrape a new file every time?

    for paper in papers:
        paper.scrape_data()
        data.save('Papers', paper, search_term)





def collect_prs(database, pr_count):

    # crawl() AND collect a bunch of urls

    prs = []
    for url in urls:
        prs.append(base.Press_Release(url))

    for pr in prs:
        pr.scrape_data()
        data.save('PRs', pr, database)
