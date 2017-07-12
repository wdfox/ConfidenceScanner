
import base
import requester
import urls
from scripts.scripts import collect_papers, collect_prs

""" Tests for scraping """

# PubMed

# search = urls.build_search("aging", '3')
# ids = urls.get_ids(search)
# print(ids)

# fetch = urls.build_fetch(ids[0])
# print(fetch)

# paper = base.Paper(ids[0])
# print("Paper id is", paper.id)

# paper.scrape_data()
# print("Paper title is", paper.title)
# print("Paper author(s):", paper.authors)
# print("Paper journal:", paper.journal)
# print("Paper year:", paper.year)
# print("Paper abstract: \n", paper.text)



# NIH Database

# pr = base.Press_Release("https://www.nih.gov/news-events/news-releases/pregnancy-diet-high-refined-grains-could-increase-child-obesity-risk-age-7-nih-study-suggests")

# pr.scrape_data()
# print("PR title is", pr.title)
# print("PR source:", pr.source)
# print("PR year:", pr.year)
# print("PR content:\n", pr.text)


# NIH Crawler

# urls.crawl("https://www.nih.gov/news-events/news-releases")


# Paper and PR Mass collection

# papers = collect_papers(paper_count='3', search_term='aging')
# prs = collect_prs(pr_count='10', db_url="https://www.nih.gov/news-events/news-releases")






"""
test for funny characters using this article 'https://www.nih.gov/news-events/news-releases/researchers-aim-repurpose-former-experimental-cancer-therapy-treat-muscular-dystrophy'
and paper with url: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=28609678'


save in json (use dictionary) --> look at erp_data.py for save and load methods

NOTES:
- Funny characters just seemed to get passed in and parsed like normal. Any use in removing them? Would this affect normalizing for length?
- Other study only looked at MAIN causal claims--but what if the text later works to caveat the main claim?



TO DO:

1) Save and load scraped info in json files (getting there)
2) Create method for analysis (perhaps check out nltk.sentiment package)
3) Create run script for mass paper collection (just need to test it out and work on saving)
4) Test crawl function (should be able to find 357 pages, but stops after 13)
5) Create run script for mass pr collection (should work once saving gets figured out)
6) Journal press releases versus university versus national institute?

"""
