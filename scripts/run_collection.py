"""Script to run a collection."""

import datetime
from selenium import webdriver
from consc.collection import collect_papers, collect_prs

###################################################################################################
###################################################################################################

# Set search terms
#TERMS = ['dementia', 'autism']
#COUNT = 500
TERMS = ['autism', 'dementia', 'epilepsy', 'stroke', 'parkinsons', 'optogenetics', 'bilingualism', 'consciousness', 'perception', 'cognition', 'vaccines', 'coma', 'diabetes', 'hypertension']
COUNT = 1000

# Set the start & end date
# START_DATE = datetime.date(year=2017, month=5, day=7)
# END_DATE = datetime.date(year=2017, month=12, day=31)
START_DATE = datetime.date(year=2017, month=1, day=1)
END_DATE = datetime.date(year=2017, month=12, day=31)

###################################################################################################
###################################################################################################

def main():

	driver = webdriver.Safari()

	# Collect papers & press-releases
	for term in TERMS:
		collect_papers(search_term=term, start_date=START_DATE, end_date=END_DATE, paper_count=COUNT, use_hist=True)
		print(term, 'papers collected')
		collect_prs(search_term=term, start_date=START_DATE, end_date=END_DATE, driver=driver, pr_count=COUNT)
		print(term, 'prs collected')

	driver.close()


if __name__ == '__main__':
	main()
