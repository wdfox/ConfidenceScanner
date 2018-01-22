'''Test cases for Com_Scanner classes and functions'''

import base
import requester
import urls
import data
from scripts.scripts import collect_papers, collect_prs

import datetime
from bs4 import BeautifulSoup


""" Tests for scraping """

##############
### PubMed ###
##############


### Single ID Check ###

# ids = ['28800331']
# print(type(ids))

# fetch = urls.build_fetch(ids)
# print(fetch)

# paper = base.Paper('28800331')
# req = requester.Requester()
# # Use Requester() object to open the paper URL
# art_page = req.get_url(fetch)

# # Get paper into a more convenient format for info extraction
# page_soup = BeautifulSoup(art_page.content, 'lxml')

# # Pull out articles
# articles = page_soup.find_all('pubmedarticle')
# paper.extract_add_info(articles[0])
# print(paper.text)


### E-Info ###

# einfo = urls.build_info()
# print(einfo)

# # Initialize a requester object to handle URL calls
# req = requester.Requester()

# # Get the URL for the database EInfo call
# page = req.get_url(einfo)

# # More convenient form for extraction
# page_soup = BeautifulSoup(page.content, 'lxml')

# print(page_soup.dbname.text)


### Search, Fetch, and Extract ###

# search = urls.build_search("aging", '3')
# ids = urls.get_ids(search)
# print(ids)

# fetch = urls.build_fetch(ids)
# print(fetch)

# paper = base.Paper(ids[1])
# print("Paper id is", paper.id)

# paper.scrape_data()
# print("Paper doi is", paper.doi)
# print("Paper title is", paper.title)
# print("Paper author(s):", paper.authors)
# print("Paper journal:", paper.journal)
# print("Paper year:", paper.year)
# print("Paper abstract: \n", paper.text)

# info_dict = paper.__dict__()
# print(type(info_dict))
# print(info_dict)


###################
### Use History ###
###################

# search = urls.build_search('aging', '3', use_hist=True)
# print(search)
# info = urls.get_use_hist(search)
# print(info)

# collect_papers(paper_count='3', search_term='aging', use_hist=True)


###################
### EurekAlert! ###
###################

# data.scrape_pr_data(url='https://www.eurekalert.org/pub_releases/2017-08/uoc--lbb080817.php', path=None)
# data.scrape_pr_data(url='https://www.eurekalert.org/pub_releases/2017-11/brf-sfn112817.php', path=None)

# end_date = datetime.date.today()
# start_date = end_date.replace(day=end_date.day-6)

# collect_prs(search_term='aging', start_date=start_date, end_date=end_date)


################
### Analysis ###
################
# search = urls.build_search('aging', '1')
# ids = urls.get_ids(search)
# print(ids)
# fetch = urls.build_fetch(ids)
# print(fetch)

# paper = base.Paper(ids[0])
# paper.scrape_data()
# paper.analyze()


####################
### NIH Database ###
####################

# pr = base.Press_Release("https://www.nih.gov/news-events/news-releases/pregnancy-diet-high-refined-grains-could-increase-child-obesity-risk-age-7-nih-study-suggests")

# pr.scrape_data()
# print("PR title is", pr.title)
# print("PR source:", pr.source)
# print("PR year:", pr.year)
# print("PR content:\n", pr.text)


###################
### NIH Crawler ###
###################

# urls.crawl(search_term='aging', start_date=None, end_date=None)


####################################
### Paper and PR Mass collection ###
####################################

# papers = collect_papers(paper_count='3', search_term='aging')
# prs = collect_prs(pr_count='10', db_url="https://www.nih.gov/news-events/news-releases")


################################
### Save and Load Procedures ###
################################

# outfile = data.assign_outfile(index=0)
# print(outfile)

# paper_path = data.build_path('Papers', 'aging') + '/0001.json'
# paper = data.load_paper_json(paper_path)
# print(paper.id)

paper_list = data.load_folder('Papers', 'autism')
# print(paper_list)
# print(len(paper_list))


"""

NOTES:
- Other study only looked at MAIN causal claims--but what if the text later works to caveat the main claim?


Read 2014 Sumner Paper and anything from reference list on Tom's paper by relevance
Look at Google Scholar for relevant papers maybe?
Read papers from tom
Try out sentiment analysis (out of the box nltk) try using a jupyter notebook (scores for text difficulty, sentiment, etc.) maybe textblob
PR Scraping
What kinds of analysis to run

"""
