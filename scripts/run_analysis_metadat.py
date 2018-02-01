"""  """

import os
from itertools import chain

import pandas as pd

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

    for dat_type in DAT_TYPES:

        print('Running ', dat_type)

        # Initialize dataframe
        df = pd.DataFrame(columns=['id', 'term', 'n_words', 'has_source_link', 'has_article_link',
                                   'has_other_link', 'region', 'journal'])

        for term in TERMS:

            print('\tRunning ', term)

            # Load the data
            docs = load_folder(dat_type, term, DAT_PATH, proc_text=True)

            for ind, doc in enumerate(docs):

                # Skip any documents that have no text
                if not doc.text:
                    continue

                # Set unique identifier for each doc
                if dat_type == 'Papers':
                    uid = doc.id
                if dat_type == 'PRs':
                    uid = term[:3] + str(ind)

                # Genera meta-data
                n_words = len(list(chain(*doc.tokens)))

                # PR specific meta-data
                if dat_type == 'PRs':

                    has_source_link = True if doc.source_link else False
                    has_article_link = True if doc.article_link else False

                    other_link = True if 'http' in doc.text else False
                    has_other_link = True if other_link else False

                    journal = doc.journal
                    region = doc.region

                # Paper specific meta-data
                elif dat_type == 'Papers':
                    has_source_link, has_article_link, has_other_link = None, None, None
                    region = None
                    journal = doc.journal[0]

                # Append to dataframe
                df = df.append({'id' : uid,
                                'term' : term,
                                'n_words' : n_words,
                                'has_source_link' : has_source_link,
                                'has_article_link' : has_article_link,
                                'has_other_link' : has_other_link,
                                'region' : region,
                                'journal' : journal
                                }, ignore_index=True)

            df.to_csv(os.path.join('results', dat_type + '_metadata.csv'), index=False)

if __name__ == '__main__':
    main()
