'''Functions for using Selenium Webdriver for webpage emulation and scraping'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Safari()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name('q')
# elem.clear()
# elem.send_keys('pycon')
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()


def pr_crawl(pr_count, search_term):

	# Initialize a webdriver so Selenium can emulate the page
	driver = webdriver.Safari()

	# Access EurekAlert!'s Advanced Search page'
	driver.get('https://www.eurekalert.org/search.php')


	# End the browser instance
	driver.close()