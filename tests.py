
import base
import requester
import urls

""" Tests for scraping """

# # PubMed

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



# # NIH Database

# pr = base.Press_Release()

# pr.scrape_data()
# print("PR title is", pr.title)
# print("PR source:", pr.source)
# print("PR year:", pr.year)
# print("PR content:\n", pr.text)


# NIH Crawler

base.crawl()