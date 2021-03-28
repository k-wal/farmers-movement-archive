import re
import sys
import os
import requests
import json
import datetime
import numpy as np
import pickle

params = {
    'key_identity': 'Xz9kFHaoaCaCKIz9Ez2UNjgBkLxLmZqg',
    'key_credential': 'dJsaJ18IZB25GYEwWzMadmT0G1CskF2y'
}

item_set_id = {
11:9314
}

def upload_article(date, item_set_id, title, description, url, username, user_url, tweet_id):
	headers = {
	'Content-type': 'application/json'
	}


	data = {
		"dcterms:title" : [{"property_id" : 1, "property_label" : "Title", "@value" : title, "type" : "literal"}],
		"dcterms:description" : [{"property_id" : 4, "property_label" : "Description", "@value" : description, "type" : "literal"}],
		"dcterms:source" : [{"property_id" : 11, "property_label" : "Source", "@id" : url, "type" : "uri"}],
		#"dcterms:publisher" : [{"property_id" : 5, "property_label" : "Publisher", "@value" : publisher, "type" : "literal"}],
		"dcterms:date" : [{"property_id" : 7, "property_label" : "Date", "@value" : date, "type" : "literal"}],
		"dcterms:contributor" : [{"property_id" : 6, "property_label" : "Contributor", "o:label" : username, "@id" : user_url, "type" : "uri"}],
		"dcterms:identifier" : [{"property_id" : 10, "property_label" : "Identifier", "@value" : tweet_id, "type" : "literal"}],
		#"dcterms:coverage" : [{"property_id" : 14, "property_label" : "Coverage", "@value" : location, "type" : "literal"}],
		"o:resource_class" : {"o:id" : 72} ,
		"@type" : "o:Item",
		"o:item_set" : [ {"o:id": item_set_id}], 
		"o:media" : []
	}

	response = requests.post('http://indiasocialarchive.iiit.ac.in/api/items', headers=headers, params=params, data=json.dumps(data))
	j = json.loads(response.text)
	#print(j)


def if_upload(date, tweet_id):
	tweet_id = int(tweet_id)
	month = date.split('-')[1]
	dir_path = 'ids/'
	filenames = os.listdir(dir_path)
	max_per_file = 5000

	cur_filepath = ''

	for filename in filenames:
		filepath = dir_path + filename

		with open(filepath, 'rb') as f:
			arr = pickle.load(f)

		if tweet_id in arr:
			return False

		if arr.size < max_per_file and cur_filepath == '':
			cur_filepath = filepath

	if cur_filepath == '':
		new_filename = str(len(filenames) + 1) + '.pkl'
		cur_filepath = dir_path + new_filename
		print("INITIALIZING NEW : " + cur_filepath)
		cur_arr = np.array([])
	else:
		with open(cur_filepath, 'rb') as f:
			cur_arr = pickle.load(f)

	cur_arr = np.append([tweet_id],cur_arr)
	with open(cur_filepath, 'wb') as f:
		pickle.dump(cur_arr, f)
	return True

def upload_file(filepath, item_set_id):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()
	total = len(lines)
	for index, line in enumerate(lines):
		parts = line.split('|-|')
		date, tweet_id, username, text, url = parts[0].strip(), parts[1].strip(), parts[3].strip(), parts[7].strip(), parts[8].strip()
	
		if if_upload(date,tweet_id):
			user_url = url.split('/status/')[0]
			if len(text) > 30:
				desc = text[0:30] + " . . . . "
			else:
				desc = text
			title = "<em>" + username + "</em> : " + desc
			upload_article(date, item_set_id, title, text, url, username, user_url, tweet_id)
		if index % 10 == 0:
			print(str(index) + " of " + str(total) + " done")


def upload_section(dir_path, item_set_id):
	filenames = os.listdir(dir_path)
	for filename in filenames:
		path = dir_path + '/' + filename
		print(filename + " : begin")
		upload_file(path, item_set_id)
		print(filename + " : end")

filepath = '../../corpus/temp_tweets/farmbill/11-2020.txt'
upload_file(filepath, item_set_id[11])