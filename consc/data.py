''' Functions for saving and loading data into json file format '''

import base
import json
import os
import datetime
from requester import Requester

from bs4 import BeautifulSoup
from shutil import copy2

def scrape_paper_data(url, path, retstart=0):
	"""Retrieve the paper from PubMed and extract the info.

	Parameters
	----------
	url : str
		Fetch URL for the desired papers
	path : str
		Path to the save location for scraped data
	ret_start : int
		An integer for keeping track of the saving index (so papers don't get saved over others if using history)
	"""

	# Initialize Requester object for URL requests
	req = Requester()

	# Use Requester() object to open the paper URL
	art_page = req.get_url(url)

	# Get paper into a more convenient format for info extraction
	page_soup = BeautifulSoup(art_page.content, 'lxml')

	# Pull out articles
	articles = page_soup.find_all('pubmedarticle')

	# Loop through articles
	for ind, article in enumerate(articles):

		# For each article, pull the ID and extract relevant info
		art_id = article.find('articleid', idtype='pubmed').text
		paper = base.Paper(art_id)
		paper.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
		paper.extract_add_info(article)

		# Ensure all attributes are of the correct type
		paper._check_type()

		# Save paper object to JSON file
		outfile = '{:04d}.json'.format(ind+retstart)
		save(path, outfile, paper)

	# Close the URL request
	req.close()


def scrape_pr_data(url, path):
	"""Retrieve the press release from Eurekalert and extract the info.

	Parameters
	----------
	url : str
		Fetch URL for the desired press release
	path : str
		Path to the save location for scraped data
	"""

	# Initialize Requester object for URL requests
	req = Requester()

	# Use Requester() to open the press release URL
	art_page = req.get_url(url)

	# Get press release into a more convenient format for info extraction
	page_soup = BeautifulSoup(art_page.content, 'lxml')

	# Initialize a press release object to store the scraped data and extract info
	pr = base.Press_Release(url)
	pr.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
	pr.extract_add_info(page_soup)

	# Close the URL request
	req.close()

	# Ensure all attributes are of the correct type
	pr._check_type()

	return(pr)


def build_path(data_type, search_term, batch=None, root_dir='Data/'):
	"""Gives the path to the save locations of paper or pr objects

	Parameters
	----------
	data_type : str
		Type of data (Paper or Press_Release) to be found
	search_term : str
		PubMed search term (papers) or government database (press releases) used to find the given info
	root_dir : str
		Directory that the JSON files will be saved under

	Returns
	-------
	path : str
		Path to the data stored matching the given parameters
	"""

	# Join the elements together to create the desired path
	path = os.path.join(root_dir, data_type, search_term)

	# For press releases add on the batch number
	if batch is not None:
		path = os.path.join(path, batch)

	# If the path does exist, ask the user if they are okay with overwriting data
	if os.path.isdir(path):
		clear_db(path)

	# If the path doesn't already exist in the system, make it
	elif not os.path.isdir(path):
		os.makedirs(path)

	return(path)


def clear_db(path):
	"""Ensures existing data is not accidentally overwritten by new scrapes

	Parameters
	----------
	path : str
		Path to the save location for scraped data

	Notes
	-----
	"""
	overwrite = input('You may be overwriting saved data. Continue? (y/n) \n > ')

	# If the user does want to overwrite data, temporary archive existing data and empty the directory
	if overwrite == 'y':
		
		# Create temporary archive
		archive = os.path.join('Data', 'Archive')

		# Archive and delete files
		for file in os.listdir(path):
			file_path = os.path.join(path, file)
			
			# Copy the db contents into the temporary archive
			copy2(file_path, archive)

			# Delete all files in the directory where new data will be saved
			os.unlink(file_path)
	
	# If user does not want to overwrite data, raise an error and quit
	elif overwrite =='n':
		raise RuntimeError('Save function quit to avoid overwriting existing data')

	# If user enters any other characters, show the prompt again
	else:
		clear_db(path)


def clear_archive():
	"""Deletes all archived files"""

	# Create the path to the saved data archive
	archive = os.path.join('Data', 'Archive')

	# Delete all files in the archive
	for file in os.listdir(archive):
		file_path = os.path.join(archive, file)
		os.unlink(file_path)


def save(path, outfile, data):
	"""Saves data from paper or press release object to JSON

	Parameters
	----------
	path : str
		Path to the desired save location by data type and search term
	outfile : str
		Filename associated with a given paper for organizational purposes
	data : Paper object or Press_Release object
		Extracted info from the paper or press release
	"""

	# Build the path for the individual file to be saved at
	file_path = os.path.join(path, outfile)

	# Convert our information into a savable dictionary format
	info_dict = data.__dict__()

	# Save information to the path generated, each entry on its own line
	with open(file_path, 'w') as outfile:
		json.dump(info_dict, outfile)


def load_folder(data_type, search_term, root_dir='Data/'):
	"""Load paper or press release info from an entire directory for analysis

	Parameters
	----------
	data_type : str
		Type of data (Paper or Press_Release) to be saved
	search_term : str
		PubMed search term (papers) or government database (press releases) used to find the given info
	root_dir : str
		Directory that the JSON files are saved under

	Returns
	-------
	items : list of Paper or Press_Release objects
		List of all papers or prs saved in a given directory

	Notes
	-----
	- For a given type and search term, check the available files and load each one into a paper or pr object
	"""

	# Give the path to the desired directory
	directory = os.path.join(root_dir, data_type, search_term)

	items = []

	if data_type == 'Papers':

		# List all files in the directory
		files = os.listdir(directory)

		# Remove hidden files from the directory (if present) and db_info file, leaving only paper or pr files
		files = [f for f in files if f[0] in '0123456789']

		for ind, file in enumerate(files):
			path = os.path.join(directory, file)

			paper = load_paper_json(path)
			items.append(paper)

	elif data_type == 'PRs':

		folders = os.listdir(directory)

		folders = [fol for fol in folders if fol[0] in '0123456789']

		files = []

		for fol in folders:

			cur_directory = os.path.join(directory, fol)

			files = os.listdir(cur_directory)

			files = [f for f in files if f[0] in '0123456789']

			for ind, file in enumerate(files):

				path = os.path.join(cur_directory, file)

				pr = load_pr_json(path)
				items.append(pr)


	# # Initialize a list to store the paper or press release objects generated
	# items = [None] * len(files)

	# # Go through directory, loading each file into an individual object, append to items
	# for ind, file in enumerate(files):
	# 	path = os.path.join(directory, file)
	# 	elif data_type == 'PRs':
	# 		pr = load_pr_json(path)
	# 		items[ind] = pr

	# Filter out papers with no abstract text, redundant with above inside loop isinstance call
	items = [paper for paper in items if paper.text is not None]

	return(items)


def load_paper_json(path):
	"""Load an individual paper object from JSON file

	Parameters
	----------
	path : str
		Path to the save location of the desired paper to load

	Returns
	-------
	paper : Paper object
		Paper object with attributes populated from the JSON file
	"""

	# Retrieve the JSON file
	with open(path) as file:
		info_dict = json.load(file)

	# Populate the paper attributes
	paper = base.Paper(info_dict['id'])
	paper.doi = info_dict['doi']
	paper.title = info_dict['title']
	paper.authors = info_dict['authors']
	paper.journal = info_dict['journal']
	paper.text = info_dict['text']
	paper.sentences = info_dict['sentences']
	paper.words = info_dict['words']
	paper.year = info_dict['year']
	paper.date = info_dict['date']

	return(paper)


def load_pr_json(path):
	"""Load an individual Press_Release object from JSON file

	Parameters
	----------
	path : str
		Path to the save location of the desired press release to load

	Returns
	-------
	pr : Press_Release object
		Press_Release object with attributes populated from the JSON file
	"""

	# Retrieve the JSON file
	with open(path) as file:
		info_dict = json.load(file)

	# Populate the pr attributes
	pr = base.Press_Release(info_dict['url'])
	pr.title = info_dict['title']
	pr.text = info_dict['text']
	pr.sentences = info_dict['sentences']
	pr.words = info_dict['words']
	pr.source = info_dict['source']
	pr.year = info_dict['year']
	pr.date = info_dict['date']

	return(pr)
