
''' Functions for saving and loading data into json file format '''

import base
import json



# import os

# # NOT SUPER PORTABLE BETWEEN USERS - should I even do it this way?
# def save_location(search_type, search_term):
	
# 	# Search term refers to a specific keywork if search_type is paper or a specific pr database if the type is pr
#     base = 'Users/wdfox/Documents/GitCode/Confidence_Scanner/Data/'
#     path = base + str(search_type) + '/' + str(search_term)

#     if not os.path.isdir(path):
#         os.makedirs(path)

#     return(path)


def save(data_type, search_term, data):
    """Saves data from paper or press release object to JSON

    Parameters
    ----------
    data_type : str
        Type of data (Paper or Press_Release) to be saved
    search_term : str
        PubMed search term (papers) or government database (press releases) used to find the given info
    data : Paper object or Press_Release object
        Extracted info from the paper or press release

    Notes
    -----
    - Doesn't really work as expected right now
    - The problem could be here, or perhaps in the scripts file... Not sure...
    """

    # Convert our information into a savable dictionary format
    info_dict = data.__dict__
    # Get rid of the reqester object, which is unable to be saved directly to JSON
    del info_dict['req']

    # Save information to the path generated, each entry on its own line
    with open('/Users/wdfox/Documents/GitCode/Confidence_Scanner/Data/' + data_type + '/' + search_term + '.json', 'w') as outfile:
        json.dump(info_dict, outfile)
        outfile.write('\n')


def load(data_type, search_term):
    """Load paper and press release info for analysis

    Parameters
    ----------
    data_type : str
        Type of data (Paper or Press_Release) to be saved
    search_term : str
        PubMed search term (papers) or government database (press releases) used to find the given info

    Notes
    -----
    - This function is a long way from being ready to use
    """

    filename = 'Users/wdfox/Documents/GitCode/Confidence_Scanner/Data/' + data_type + '/' + search_term + '.json'
    
    for l in open(filename):
        yield json.loads(l)

    # All of this is very speculative right now
    # Once I recover my original dictionary:
    papers = []

    for line in json_file:
        
        info_dict = {}
        
        if data_type == 'Paper':
            paper = base.Paper(info_dict['id'])
            paper.title = info_dict['title']
            paper.authors
            paper.journal
            paper.text = info_dict['text']
            paper.year = info_dict['year']
            paper.date = info_dict['date']

        elif data_type == 'PR':
            pr = base.Press_Release(info_dict['url'])
            pr.title
            pr.source
            pr.text
            pr.year
            pr.date

