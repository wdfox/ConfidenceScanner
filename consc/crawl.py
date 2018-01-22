'''Functions for using Selenium Webdriver for webpage emulation and scraping'''

import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



def pr_crawl(pr_count, search_term, start_date, end_date):

	# Initialize a webdriver so Selenium can emulate the page
	driver = webdriver.Safari()

	# Parse out individual components from given start dates for search
	start_day = str(start_date.day)
	start_month = str(start_date.month)
	start_year = str(start_date.year)
	# And end dates
	end_day = str(end_date.day)
	end_month = str(end_date.month)
	end_year = str(end_date.year)

	# Creat the search URL based on the term and dates desired
	crawl_base = 'https://srch.eurekalert.org/e3/query.html?qs=EurekAlert&pw=100.101%25&op0=%2B&fl0=&ty0=w&tx0='
	crawl_middle = '&op1=%2B&fl1=institution%3A&ty1=p&tx1=&op2=%2B&fl2=journal%3A&ty2=p&tx2=&op3=%2B&fl3=meeting%3A&ty3=p&tx3=&op4=%2B&fl4=region%3A&ty4=p&tx4=&op5=%2B&fl5=type%3A&ty5=p&tx5=&inthe=604800&dt=ba'

	crawl_url = crawl_base + search_term + crawl_middle + '&amo=' + start_month + '&ady=' + start_day + '&ayr=' + start_year + '&bmo=' + end_month + '&bdy=' + end_day + '&byr=' + end_year + '&op6=&fl6=keywords%3A&ty6=p&rf=1'

	# Go to first page containing press releases
	driver.get(crawl_url)

	# Loop through pages containing article links
	pages_continue = True
	page_num = 1

	# Initialize a list to store the pr links as we loop
	pr_links = []
	while pages_continue:

		# Initialize a list to store links from this page of the crawl only
		page_links = []

		# Get the source code for the page
		page = driver.page_source
		page_soup = BeautifulSoup(page, 'lxml')
		results = page_soup.select(".results")
		links = results[0].find_all("a")

		i = 0
		for link in links[1:]:

			link = link["href"]
			if link[0:2] == 'cs' and len(pr_links) < pr_count:
				try:
					link_start = link.find('pub_releases')
					link_end = link.find('php')
					pr_links.append(link[link_start : link_end + 3])
				except:
					page_links.append('')

			elif len(pr_links) == pr_count:
				driver.close()
				print(len(pr_links))
				return pr_links

		# Increment the page number to continue search
		page_num += 1

		# Page numbers are a bit gimmicky (single digit different than double), but this works
		if page_num < 10:
			page_str = ' ' + str(page_num)
		else:
			page_str = str(page_num)

		try:
			# Find button for next page
			next_page = driver.find_element(By.LINK_TEXT, page_str)
			next_page.click()

			# No accidental DDoS attacks
			sleep_time = random.uniform(4.0, 5.0)
			time.sleep(sleep_time)

		except:
			pages_continue = False

	# End the browser instance
	driver.close()

	return pr_links


# pr_crawl(27, 'https://srch.eurekalert.org/e3/query.html?qs=EurekAlert&pw=100.101%25&op0=%2B&fl0=&ty0=w&tx0=aging&op1=%2B&fl1=institution%3A&ty1=p&tx1=&op2=%2B&fl2=journal%3A&ty2=p&tx2=&op3=%2B&fl3=meeting%3A&ty3=p&tx3=&op4=%2B&fl4=region%3A&ty4=p&tx4=&op5=%2B&fl5=type%3A&ty5=p&tx5=&inthe=604800&dt=ba&amo=1&ady=9&ayr=2017&bmo=1&bdy=16&byr=2017&op6=&fl6=keywords%3A&ty6=p&rf=1')


# driver = webdriver.Safari()
# driver.get('https://srch.eurekalert.org/e3/query.html?qs=EurekAlert&pw=100.101%25&op0=%2B&fl0=&ty0=w&tx0=aging&op1=%2B&fl1=institution%3A&ty1=p&tx1=&op2=%2B&fl2=journal%3A&ty2=p&tx2=&op3=%2B&fl3=meeting%3A&ty3=p&tx3=&op4=%2B&fl4=region%3A&ty4=p&tx4=&op5=%2B&fl5=type%3A&ty5=p&tx5=&inthe=604800&dt=ba&amo=1&ady=9&ayr=2017&bmo=1&bdy=16&byr=2017&op6=&fl6=keywords%3A&ty6=p&rf=1')
# print("Driver works")
# next_page = driver.find_element(By.LINK_TEXT, '10')
# print("Next page element exists")


# NOTE:
# Format for 1-9: ' x'
# Format for 10- : 'xx'




