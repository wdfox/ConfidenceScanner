"""Script to Analyze Data"""

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

	papers_analyzed = {'readability' : {}, 'vader_sentiment' : {}, 'liu_hu_sentiment' : {}, 'subjectivity' : {}, 'confidence' : {}}
	press_analyzed = {'readability' : {}, 'vader_sentiment' : {}, 'liu_hu_sentiment' : {}, 'subjectivity' : {}, 'confidence' : {}}

	for term in TERMS:

		# Load papers and press releases into analyzable format
		papers = load_folder('Papers', term)
		press = load_folder('PRs', term)

		# Run readability 
		papers_analyzed['readability'][term] = None
		press_analyzed['readability'][term] = None

		# Run VADER sentiment analysis
		papers_analyzed['vader_sentiment'][term] = vader_folder(papers)
		press_analyzed['vader_sentiment'][term] = vader_folder(press)

		# Run Liu Hu sentiment analysis
		papers_analyzed['liu_hu_sentiment'][term] = liu_folder(papers)
		press_analyzed['liu_hu_sentiment'][term] = liu_folder(press)

		# Run subjectivity analysis
		papers_analyzed['subjectivity'][term] = folder_subjectivity(papers)
		press_analyzed['subjectivity'][term] = folder_subjectivity(press)

		# Run LIWC confidence analysis
		papers_analyzed['confidence'][term] = folder_confidence(papers)
		press_analyzed['confidence'][term] = folder_confidence(press)

	return papers_analyzed, press_analyzed


if __name__ == '__main__':
	main()

