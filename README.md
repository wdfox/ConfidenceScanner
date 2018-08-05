# Confidence Scanner

## General
The Confidence Scanner is a project for automated collection and analysis of scientific text samples. The functionality can be broken into two primary steps. In the data collection phase, paper abstracts are gathered from PubMed, a repository for scientific papers specifically in Medicine and the Life Sciences, and press releases are scraped from EurekAlert, a public database for scientific press releases from a variety of research institutions and fields. Analysis consists of four different tests--Readability, Sentiment, Subjectivity, and Confidence. A paper written for the CogSci 2018 conference further detailing the analysis can be found [here](http://mindmodeling.org/cogsci2018/papers/0324/index.html) and a conference poster can be found [here](https://www.dropbox.com/s/1w2f920506k02r0/Fox%26Donoghue_ConfidenceScanner_CogSciPoster.pdf?dl=0).

## Organization and Usage

### consc
Contains all functionality for web scraping both using the PubMed EUtils API and EurekAlert's Advanced Search feature. 

### analysis
Readability is based primarily around the Flesch-Kincaid Reading Ease score, although calculation is also done for other measures of textual difficulty such as SMOG Index. Sentiment is measured using both the VADER and Liu Hu lexicons, independently shown to indicate the polarity of text samples. Subjectivity is measured with an SVM trained on NLTK's built in subjectivity lexicon. Confidence  analysis utilizes a Linguistic Inquiry and Word Count (LIWC) method with a lexicon curated by the researchers. 

### scripts
Scripts are separated into analysis and collection. The collection script can be run to retrieve press releases and paper abstracts for given search terms published in a desired date range. The analysis scripts can be run on this data. 

### data
The data used in the writing of the paper is available in the Data folder on GitHub. 

## Development
Functions were developed and tested in Python 2.7 and Python 3.4, and may not be fully compatible with other versions of Python. 

Software developed in collaboration with Tom Donoghue and the lab of Professor Voytek at UC San Diego and takes some inspiration from ERP_SCANR: https://github.com/TomDonoghue/ERP_SCANR. 

Constructive criticism, corrections, and potential improvements are welcome.

E-mail: wdfox{at}mit{dot}edu

## Citation
If this software was useful for your work, please credit it by citing our paper:

> W. FOX, T. DONOGHUE. Confidence Levels in Scientific Writing: Automated Mining of Primary Literature and Press Releases. Cognitive Science Society. Madison, WI, USA, 2018.

## Dependencies
* NumPy
* NLTK
* BeautifulSoup
* Selenium
* textstat (Python 2.7 Only)
