
import base
import requester
import urls

""" Tests for scraping """

# PubMed

# search = urls.build_search("aging")
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

# urls.crawl()






"""
test for funny characters using this article 'https://www.nih.gov/news-events/news-releases/researchers-aim-repurpose-former-experimental-cancer-therapy-treat-muscular-dystrophy'
and paper with url: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=28609678'


save in json (use dictionary) --> look at erp_data.py for save and load methods


TO DO:

1) Save and load scraped info in json files (getting there)
2) Check how funny characters get handled (should be straight-forward)
3) Create method for analysis
4) Create run script for mass paper collection (just need to test it out and work on saving)
5) Write function to cycle through NIH website and collect urls (almost done)
6) Create run script for mass pr collection (reliant on the above, should be easy after that is figured out)

"""
