"""  """

import numpy as np
from textstat.textstat import textstatistics

from consc.data import load_folder
from consc.analysis.readability import fk_grade_group, smog_group, consensus_group, ar_group

##
##

DAT_PATH = '/Users/tom/Documents/GitCode/Confidence_Scanner/Data/'

with open('terms.txt', 'r') as terms_file:
    TERMS = terms_file.read().splitlines()

##
##

def main():

    for term in TERMS:

        print('Currently Analyzing: ', term)

        # Load the data
        paper_dat = load_folder('Papers', term, DAT_PATH, proc_text=False)
        press_dat = load_folder('PRs', term, DAT_PATH, proc_text=False)

        # Drop any docs with empty text
        paper_dat = [doc for doc in paper_dat if doc.text]
        press_dat = [doc for doc in press_dat if doc.text]

        # Flesh-Kincaid Grade Score
        fks_papers = fk_grade_group(paper_dat)
        np.save('results/' + term + '_fk_papers', np.array(fks_papers))
        fks_press = fk_grade_group(press_dat)
        np.save('results/' + term + '_fk_press', np.array(fks_press))

        # # Smog Score
        # smog_papers = smog_group(paper_dat)
        # smog_press = smog_group(press_dat)

        # # Consensus Score
        # consen_papers = consensus_group(paper_dat)
        # consen_press = consensus_group(press_dat)

        # # Automated Readability Score
        # ar_papers = ar_group(paper_dat)
        # ar_press = ar_group(press_dat)


if __name__ == '__main__':
    main()