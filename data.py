''' Functions for saving and loading data into json file format '''

import json


def save(type_of_data, data_to_write, where_to_write_it_to):
	with open('something_about_data.json', 'w') as outfile:
		json.dump(data, outfile)
		outfile.write('\n')


def load():
	pass