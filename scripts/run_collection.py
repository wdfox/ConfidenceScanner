"""Script to run a collection."""

import datetime
from consc.collection import collect_papers, collect_prs

###################################################################################################
###################################################################################################

# Set search terms
#TERMS = ['dementia', 'autism']
#COUNT = 500
TERMS = ['aging']
COUNT = 30

# Set the start & end date
START_DATE = datetime.date(year=2017, month=1, day=1)
END_DATE = datetime.date(year=2017, month=1, day=14)
#START_DATE = datetime.date(year=2017, month=1, day=1)
#END_DATE = datetime.date(year=2017, month=12, day=31)

###################################################################################################
###################################################################################################

def main():

    # Collect papers & press-releases
    for term in TERMS:
        collect_papers(search_term=term, start_date=START_DATE, end_date=END_DATE, paper_count=COUNT, use_hist=True)
        #collect_prs(search_term=term, start_date=START_DATE, end_date=END_DATE, pr_count=COUNT)

if __name__ == '__main__':
    main()
