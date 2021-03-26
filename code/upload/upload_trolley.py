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

item_set_dict = {2 : 6588,
3 : 6589,
4 : 6590,
5 : 6608}

def upload_article(date, item_set_id, title, description, url, publisher, location, author):
	headers = {
	'Content-type': 'application/json'
	}

	data = {
		"dcterms:title" : [{"property_id" : 1, "property_label" : "Title", "@value" : title, "type" : "literal"}],
		"dcterms:description" : [{"property_id" : 4, "property_label" : "Description", "@value" : description, "type" : "literal"}],
		"dcterms:source" : [{"property_id" : 11, "property_label" : "Source", "@id" : url, "type" : "uri"}],
		"dcterms:publisher" : [{"property_id" : 5, "property_label" : "Publisher", "@value" : publisher, "type" : "literal"}],
		"dcterms:date" : [{"property_id" : 7, "property_label" : "Date", "@value" : date, "type" : "literal"}],
		"dcterms:contributor" : [{"property_id" : 6, "property_label" : "Contributor", "@value" : author, "type" : "literal"}],
		# "dcterms:created" : [{"property_id" : 20, "property_label" : "Created", "@value" : date, "type" : "literal"}],
		"dcterms:coverage" : [{"property_id" : 14, "property_label" : "Coverage", "@value" : location, "type" : "literal"}],
		"o:resource_class" : {"o:id" : 72} ,
		"@type" : "o:Item",
		"o:item_set" : [ {"o:id": item_set_id}], 
		"o:media" : []
	}

	response = requests.post('http://indiasocialarchive.iiit.ac.in/api/items', headers=headers, params=params, data=json.dumps(data))
	j = json.loads(response.text)
	#print(j)



def upload_file(filepath, item_set_id, publisher):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()
	lines = '\n'.join(lines)

	parts = lines.split('||')
	date, location, title, content, url, author = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
	if location == '---':
		location = ''
	if author == '---':
		author = ''

	upload_article(date, item_set_id, title, content, url, publisher, location, author)

def upload_section(dir_path, item_set_id, publisher):
	filenames = os.listdir(dir_path)
	for filename in filenames:
		path = dir_path + '/' + filename
		print(filename + " : begin")
		upload_file(path, item_set_id, publisher)
		print(filename + " : end")

edition = 5
dir_path = '../../corpus/trolleytimes/hindi/' + str(edition)
upload_section(dir_path, item_set_dict[edition], 'Trolley Times')
