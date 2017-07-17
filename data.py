''' Functions for saving and loading data into json file format '''

import base
import json
import os



def build_path(data_type, search_term, root_dir='Data/'):
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

    # If the path doesn't already exist in the system, make it
    if not os.path.isdir(path):
        os.makedirs(path)

    return(path)


def assign_outfile(index):
    """Assign a four digit JSON filename to save a paper or pr

    Parameters
    ----------
    index : int
        Looping index from 0, starting over each search, to ensure UNIQUE digits are assigned

    Returns
    -------
    outfile : str
        Contains the name of the file where the object will be saved

    Notes
    -----
    - All outfiles will be four digit numbers, with zeros at the start for shorter numbers
        - E.g. The fourteenth object saved will be saved at '0013.json' (indexed from '0000')
    """

    # New variable to create a string outfile name
    i = str(index)

    # Generate the proper number of zeros, given the index
    zeros = '0' * (4 - len(i))

    # Join the zeros before the index to create the save ID
    id = zeros + i

    # Save in JSON file format
    outfile = id + '.json'

    return(outfile)


def save(data_type, search_term, data, outfile):
    """Saves data from paper or press release object to JSON

    Parameters
    ----------
    data_type : str
        Type of data (Paper or Press_Release) to be saved
    search_term : str
        PubMed search term (papers) or government database (press releases) used to find the given info
    data : Paper object or Press_Release object
        Extracted info from the paper or press release
    outfile : str
        Filename associated with a given paper for organizational purposes
    """

    # Get the directory to save the data in
    directory = build_path(data_type, search_term)

    # Build the path for the individual file to be saved at
    path = os.path.join(directory, outfile)

    # Convert our information into a savable dictionary format
    info_dict = data.__dict__()

    # Save information to the path generated, each entry on its own line
    with open(path, 'w') as outfile:
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

    # List all files in the directory
    files = os.listdir(directory)
    print(files)

    # Initialize a list to store the paper or press release objects generated
    items = []

    # Go through directory, loading each file into an individual object, append to items
    if data_type == 'Papers':
        for file in files:
            path = os.path.join(directory, file)
            items.append(load_paper_json(path))
    elif data_type == 'PRs':
        for file in files:
            path = os.path.join(directory, file)
            items.append(load_pr_json(path))

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

    Notes
    -----
    - Not sure whether I should be using json.load or json.loads here
    """

    # Retrieve the JSON file
    with open(path) as file:
        info_dict = json.load(file)

    # Populate the paper attributes
    paper = base.Paper(info_dict['id'])
    paper.title = info_dict['title']
    paper.authors = info_dict['authors']
    paper.journal = info_dict['journal']
    paper.text = info_dict['text']
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

    Notes
    -----
    - Not sure whether I should be using json.load or json.loads here
    """

    # Retrieve the JSON file
    with open(path) as file:
        info_dict = json.load(file)

    # Populate the pr attributes
    pr = base.Press_Release(info_dict['url'])
    pr.title = info_dict['title']
    pr.text = info_dict['text']
    pr.source = info_dict['source']
    pr.year = info_dict['year']
    pr.date = info_dict['date']

    return(pr)

