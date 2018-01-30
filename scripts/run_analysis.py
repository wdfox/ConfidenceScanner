"""Script to Analyze Data"""

import os

import numpy as np
import pandas as pd

from consc.data import load_folder

from consc.analysis.sentiment import vader_doc, liu_polarity
from consc.analysis.subjectivity import doc_subjectivity
from consc.analysis.confidence import doc_confidence

###################################################################################################
###################################################################################################

#DAT_PATH = '/Users/wdfox/Documents/GitCode/Confidence_Scanner/Data/'
DAT_PATH = '/Users/tom/Documents/GitCode/Confidence_Scanner/Data/'

DAT_TYPES = ['PRs', 'Papers']

with open('terms.txt', 'r') as terms_file:
	TERMS = terms_file.read().splitlines()

#TERMS = ['autism', 'dementia', 'epilepsy', 'stroke', 'parkinsons', 'optogenetics', 'bilingualism',
#		 'consciousness', 'perception', 'cognition', 'vaccines', 'coma', 'diabetes', 'hypertension']
# TERMS = ['autism', dementia]

###################################################################################################
###################################################################################################

def main():

	for dat_type in DAT_TYPES:

		print('Running ', dat_type)

		# Initialize dataframe
		df = pd.DataFrame(columns=['id', 'term', 'vader', 'liu', 'subj', 'liwc'])

		for term in TERMS:

			print('\tRunning ', term)

			# Load the data
			docs = load_folder(dat_type, term, DAT_PATH, proc_text=True)
			print('\t\tLoaded')

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
				vader = vader_doc(doc)
				liu = liu_polarity(doc)
				subj = doc_subjectivity(doc)
				liwc = doc_confidence(doc)

				# Append to dataframe
				df = df.append({'id' : uid,
								'term' : term,
								'vader' : vader,
								'liu' : liu,
								'subj' : subj,
								'liwc' : liwc
								}, ignore_index=True)

				#if ind+1 % 50 == 0:
				print('\t\t', ind, 'out of', len(docs))

		df.to_csv(os.path.join('results', dat_type + '_analysis_test.csv'))


if __name__ == '__main__':
	main()

