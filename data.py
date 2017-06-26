''' Functions for saving and loading data into json file format '''

import json
import os


# NOT SUPER SURE HOW PORTABLE THIS PART OF THE CODE IS BETWEEN USERS--not that it's really that important anyway
def save_location(search_type, search_term):
	
	# Search term refers to a specific keywork if search_type is paper or a specific pr database if the type is pr
    base = 'Users/wdfox/Documents/GitCode/Confidence_Scanner/Data/'
    path = base + str(search_type) + str(search_term)

    if not os.path.isdir(path):
        os.mkdirs(path)

    return(path)

    # FINISH FIGURING OUT WHERE TO SAVE THE DIFFERENT FILES, THEN IMPLEMENT INTO THE RUN_SCRIPT




def save(type_of_data, data, search_term):
    
    
    # Need to get the data into the right format to be saved first

    path = save_location(type_of_data, search_term)

    # Convert our information into a savable dictionary format
    info_dict = data.__dict__

    with open(path + '.json', 'w') as outfile:
        json.dump(info_dict, outfile)
        outfile.write('\n')


def load():
    pass