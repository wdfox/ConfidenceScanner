"""Run readability analysis. Note: This scipt runs in py27."""

import os

import pandas as pd
from textstat.textstat import textstatistics

from consc.data import load_folder

###################################################################################################
###################################################################################################

DAT_PATH = '/Users/tom/Documents/GitCode/Confidence_Scanner/Data/'

DAT_TYPES = ['Papers', 'PRs']

with open('terms.txt', 'r') as terms_file:
    TERMS = terms_file.read().splitlines()

###################################################################################################
###################################################################################################

def main():

    # Initialize textstat object
    ts = textstatistics()

    for dat_type in DAT_TYPES:

        print('Running ', dat_type)

        # Initialize dataframe
        df = pd.DataFrame(columns=['term', 'id', 'fk', 'smog', 'consen', 'ar'])

        for term in TERMS:

            print('\tRunning ', term)

            # Load the data
            docs = load_folder(dat_type, term, DAT_PATH, proc_text=False)

            for ind, doc in enumerate(docs):

                # Skip any documents that have no text
                if not doc.text:
                    continue

                # Set unique identifier for each doc
                if dat_type == 'Papers':
                    uid = doc.id
                if dat_type == 'PRs':
                    uid = term[:3] + str(ind)

                # Calculate readability measures
                fks = ts.flesch_kincaid_ease(doc.text)
                fkg = ts.flesch_kincaid_grade(doc.text)
                smog = ts.smog_index(doc.text)
                ar = ts.automated_readability_index(doc.text)
                lwf = ts.linsear_write_formula(doc.text)

                # Append to dataframe
                df = df.append({'id' : uid,
                                'term' : term,
                                'fks' : fks,
                                'fkg' : fkg,
                                'smog' : smog,
                                'ar' : ar,
                                'lwf' : lwf
                                }, ignore_index=True)

        df.to_csv(os.path.join('results', dat_type + '_readability.csv'), index=False)


if __name__ == '__main__':
    main()
