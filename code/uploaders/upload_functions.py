import re
import sys
import os
import requests
import json
import datetime


class UploadFunctions:
	
	def __init__(self):
		self.params = {
		    'key_identity': 'Xz9kFHaoaCaCKIz9Ez2UNjgBkLxLmZqg',
		    'key_credential': 'dJsaJ18IZB25GYEwWzMadmT0G1CskF2y'
		}

	def upload_article(self, date, item_set_id, parent_set_id, title, description, url, publisher, location):
		headers = {
		'Content-type': 'application/json'
		}

		data = {
			"dcterms:title" : [{"property_id" : 1, "property_label" : "Title", "@value" : title, "type" : "literal"}],
			"dcterms:description" : [{"property_id" : 4, "property_label" : "Description", "@value" : description, "type" : "literal"}],
			"dcterms:source" : [{"property_id" : 11, "property_label" : "Source", "@id" : url, "type" : "uri"}],
			"dcterms:publisher" : [{"property_id" : 5, "property_label" : "Publisher", "@value" : publisher, "type" : "literal"}],
			"dcterms:date" : [{"property_id" : 7, "property_label" : "Date", "@value" : date, "type" : "literal"}],
			# "dcterms:created" : [{"property_id" : 20, "property_label" : "Created", "@value" : date, "type" : "literal"}],
			"dcterms:coverage" : [{"property_id" : 14, "property_label" : "Coverage", "@value" : location, "type" : "literal"}],
			"o:resource_class" : {"o:id" : 72} ,
			"@type" : "o:Item",
			"o:item_set" : [ {"o:id": item_set_id}, {"o:id" : parent_set_id}], 
			"o:media" : []
		}

		response = requests.post('http://indiasocialarchive.iiit.ac.in/api/items', headers=headers, params=self.params, data=json.dumps(data))
		j = json.loads(response.text)
		#print(j)

	def get_date_from_filename(self, name):
		date = name.split('.')[0]
		date = datetime.datetime.strptime(date, "%d-%m-%Y")
		return date.strftime("%Y-%m-%d")

	def if_upload(self, title, description, keywords):
		for keyword in keywords:
			keyword = keyword.lower()
			if ' ' in keyword:
				if keyword in title.lower():
					return True
				if keyword in description.lower():
					return True
			else:
				regex = r'\b\w+\b'
				twords = re.findall(regex, title.lower())
				dwords = re.findall(regex, description.lower())
				if keyword in twords or keyword in dwords:
					return True
		return False


	def upload_file(self, filepath, date, item_set_id, parent_set_id, publisher, location, keywords, get_location):
		file = open(filepath, 'r')
		lines = file.readlines()
		file.close()
		for line in lines:
			parts = line.split('||')
			try:
				title, description, url = parts[2], parts[3], parts[4].strip()
			except:
				print("not enough fields in line")
				continue
			location = self.get_location(parts[1])
			if self.if_upload(title, description, keywords):
				self.upload_article(date, item_set_id, parent_set_id, title, description, url, publisher, location)


	def upload_section(self, dir_path, item_set_id, parent_set_id, publisher, location, keywords, get_location):
		filenames = os.listdir(dir_path)
		filenames = sorted(filenames)
		for filename in filenames:
			path = dir_path + '/' + filename
			date = self.get_date_from_filename(filename)
			print(filename + " : begin")
			self.upload_file(path, date, item_set_id, parent_set_id, publisher, location, keywords, get_location)
			print(filename + " : end")


params = {
    'key_identity': 'Xz9kFHaoaCaCKIz9Ez2UNjgBkLxLmZqg',
    'key_credential': 'dJsaJ18IZB25GYEwWzMadmT0G1CskF2y'
}


def upload_article(date, item_set_id, parent_set_id, title, description, url, publisher, location):
	headers = {
	'Content-type': 'application/json'
	}

	data = {
		"dcterms:title" : [{"property_id" : 1, "property_label" : "Title", "@value" : title, "type" : "literal"}],
		"dcterms:description" : [{"property_id" : 4, "property_label" : "Description", "@value" : description, "type" : "literal"}],
		"dcterms:source" : [{"property_id" : 11, "property_label" : "Source", "@id" : url, "type" : "uri"}],
		"dcterms:publisher" : [{"property_id" : 5, "property_label" : "Publisher", "@value" : publisher, "type" : "literal"}],
		"dcterms:date" : [{"property_id" : 7, "property_label" : "Date", "@value" : date, "type" : "literal"}],
		# "dcterms:created" : [{"property_id" : 20, "property_label" : "Created", "@value" : date, "type" : "literal"}],
		"dcterms:coverage" : [{"property_id" : 14, "property_label" : "Coverage", "@value" : location, "type" : "literal"}],
		"o:resource_class" : {"o:id" : 72} ,
		"@type" : "o:Item",
		"o:item_set" : [ {"o:id": item_set_id}, {"o:id" : parent_set_id}], 
		"o:media" : []
	}

	response = requests.post('http://indiasocialarchive.iiit.ac.in/api/items', headers=headers, params=params, data=json.dumps(data))
	j = json.loads(response.text)
	#print(j)


def get_date_from_filename(name):
	date = name.split('.')[0]
	date = datetime.datetime.strptime(date, "%d-%m-%Y")
	return date.strftime("%Y-%m-%d")

def if_upload(title, description, keywords):
	for keyword in keywords:
		keyword = keyword.lower()
		if ' ' in keyword:
			if keyword in title.lower():
				return True
			if keyword in description.lower():
				return True
		else:
			regex = r'\b\w+\b'
			twords = re.findall(regex, title.lower())
			dwords = re.findall(regex, description.lower())
			if keyword in twords or keyword in dwords:
				return True
	return False


def upload_file(filepath, date, item_set_id, parent_set_id, publisher, location, keywords, get_location):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()
	for line in lines:
		parts = line.split('||')
		try:
			title, description, url = parts[2], parts[3], parts[4].strip()
		except:
			print("not enough fields in line")
			continue
		location = get_location(parts[1])
		if if_upload(title, description, keywords):
			upload_article(date, item_set_id, parent_set_id, title, description, url, publisher, location)


def upload_section(dir_path, item_set_id, parent_set_id, publisher, location, keywords, get_location):
	filenames = os.listdir(dir_path)
	filenames = sorted(filenames)
	for filename in filenames:
		path = dir_path + '/' + filename
		date = get_date_from_filename(filename)
		print(filename + " : begin")
		upload_file(path, date, item_set_id, parent_set_id, publisher, location, keywords, get_location)
		print(filename + " : end")
