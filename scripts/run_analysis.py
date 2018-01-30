"""Script to Analyze Data"""

import numpy as np

from consc.data import load_folder

from consc.analysis.sentiment import vader_folder, liu_folder
from consc.analysis.subjectivity import folder_subjectivity
from consc.analysis.confidence import folder_confidence

###################################################################################################
###################################################################################################

# TERMS = ['autism', 'dementia', 'epilepsy', 'stroke', 'parkinsons', 'optogenetics', 'bilingualism', 'consciousness', 'perception', 'cognition', 'vaccines', 'coma', 'diabetes', 'hypertension']
TERMS = ['autism', 'dementia']

###################################################################################################
###################################################################################################

def main():

	papers_analyzed = {'vader_sentiment' : {}, 'liu_hu_sentiment' : {}, 'subjectivity' : {}, 'confidence' : {}}
	press_analyzed = {'vader_sentiment' : {}, 'liu_hu_sentiment' : {}, 'subjectivity' : {}, 'confidence' : {}}

	for term in TERMS:

		# Load papers and press releases into analyzable format
		papers = load_folder('Papers', term)
		press = load_folder('PRs', term)

		# VADER Sentiment Analysis
		vader_papers = vader_folder(papers)
		np.save('results/' + term + '_vader_papers', np.array(vader_papers))
		vader_press = vader_folder(press)
		np.save('results/' + term + '_vader_press', np.array(vader_press))
		print('Passed VADER')

		# Liu Hu Sentiment Analysis
		liu_papers = liu_folder(papers)
		np.save('results/' + term + '_liu_papers', np.array(liu_papers))
		liu_press = liu_folder(press)
		np.save('results/' + term + '_liu_press', np.array(liu_press))
		print('Passed Liu Hu')

		# Subjectivity Analysis
		subjectivity_papers = folder_subjectivity(papers)
		np.save('results/' + term + '_subjectivity_papers', np.array(subjectivity_papers))
		subjectivity_press = folder_subjectivity(press)
		np.save('results/' + term + '_subjectivity_press', np.array(subjectivity_press))
		print('Passed Subjectivity')

		# LIWC Confidence Analysis
		confidence_papers = folder_confidence(papers)
		np.save('results/' + term + '_confidence_papers', np.array(confidence_papers))
		confidence_press = folder_confidence(press)
		np.save('results/' + term + '_confidence_press', np.array(confidence_press))
		print('Passed LIWC Confidence')

		print('Analyzed', term)

	return papers_analyzed, press_analyzed


if __name__ == '__main__':
	main()

