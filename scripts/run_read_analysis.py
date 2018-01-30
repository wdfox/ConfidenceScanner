""".  """

import os

import pandas as pd
from textstat.textstat import textstatistics

from consc.data import load_folder

##
##

DAT_PATH = '/Users/tom/Documents/GitCode/Confidence_Scanner/Data/'

DAT_TYPES = ['Papers', 'PRs']

# with open('terms.txt', 'r') as terms_file:
#     TERMS = terms_file.read().splitlines()

TERMS = ['vaccines', 'autism']

##
##

def main():

    # Initialize textstat object
    ts = textstatistics()

    for dat_type in DAT_TYPES:

        print('Running ', dat_type)

        # Initialize dataframe
        df = pd.DataFrame(columns=['term', 'fk', 'smog', 'consen', 'ar'])

        for term in TERMS:

            print('\tRunning ', term)

            # Load the data
            docs = load_folder(dat_type, term, DAT_PATH, proc_text=False)

            for ind, doc in enumerate(docs):

                # Skip any documents that have no text
                if not doc.text:
                    continue

                # Calculate readability measures
                fk = ts.flesch_kincaid_grade(doc.text)
                smog = ts.smog_index(doc.text)
                consen = ts.text_standard(doc.text)
                ar = ts.automated_readability_index(doc.text)

                # Append to dataframe
                df = df.append({'term' : term,
                                'fk' : fk,
                                'smog' : smog,
                                'consen' : consen,
                                'ar' : ar
                                }, ignore_index=True)

        df.to_csv(os.path.join('results', dat_type + '_readability.csv'), index=False)


if __name__ == '__main__':
    main()
