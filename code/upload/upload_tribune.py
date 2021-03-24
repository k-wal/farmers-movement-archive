import re
import sys
import os
import requests
import json
import datetime

params = {
    'key_identity': 'Xz9kFHaoaCaCKIz9Ez2UNjgBkLxLmZqg',
    'key_credential': 'dJsaJ18IZB25GYEwWzMadmT0G1CskF2y'
}

item_set_dict = {'nation' : 330,
'delhi' : 326,
'punjab' : 324,
'haryana' : 325,
'editorial' : 328}


def upload_article(date, item_set_id, title, description, url, publisher, location):
	headers = {
	'Content-type': 'application/json'
	}

	data = {
		"dcterms:title" : [{"property_id" : 1, "property_label" : "Title", "@value" : title, "type" : "literal"}],
		"dcterms:description" : [{"property_id" : 4, "property_label" : "Description", "@value" : description, "type" : "literal"}],
		"dcterms:source" : [{"property_id" : 11, "property_label" : "Source", "@id" : url, "type" : "uri"}],
		"dcterms:publisher" : [{"property_id" : 5, "property_label" : "Publisher", "@value" : publisher, "type" : "literal"}],
		"dcterms:date" : [{"property_id" : 7, "property_label" : "Date", "@value" : date, "type" : "literal"}],
		"dcterms:coverage" : [{"property_id" : 14, "property_label" : "Coverage", "@value" : location, "type" : "literal"}],
		"o:resource_class" : {"o:id" : 72} ,
		"@type" : "o:Item",
		"o:item_set" : [ {"o:id": item_set_id}], 
		"o:media" : []
	}

	response = requests.post('http://indiasocialarchive.iiit.ac.in/api/items', headers=headers, params=params, data=json.dumps(data))
	j = json.loads(response.text)
	#print(j)


def get_date_from_filename(name):
	date = name.split('.')[0]
	date = datetime.datetime.strptime(date, "%d-%m-%Y")
	return date.strftime("%Y-%m-%d")

def if_upload(title, description):
	return True

def upload_file(filepath, date, item_set_id, publisher, location):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()
	for line in lines:
		parts = line.split('||')
		title, description, url = parts[2], parts[3], parts[4].strip()
		if if_upload(title, description):
			upload_article(date, item_set_id, title, description, url, publisher, location)


def upload_section(dir_path, item_set_id, publisher, location):
	filenames = os.listdir(dir_path)
	for filename in filenames:
		path = dir_path + '/' + filename
		date = get_date_from_filename(filename)
		print(filename + " : begin")
		upload_file(path, date, item_set_id, publisher, location)
		print(filename + " : end")


upload_section('../../corpus/tribune/delhi', item_set_dict['delhi'], 'The Tribune', 'New Delhi')

# url = 'https://www.theweek.in/news/india/2021/01/26/violence-in-delhi-weakened-farmers-movement-aap.html'
# quote = 'The Aam Aadmi Party, which has been at the political forefront in expressing support to the farmers agitation, on Tuesday undertook a tight-rope walk as it offered its first response to the unexpected turn of events in the national capital as a large number of farmers deviated from the pre-agreed route for their tractor rally and entered central Delhi.'
# date = '2021-01-26'
# title = "Violence in Delhi weakened farmers movement: AAP"
# item_set_id = 297

