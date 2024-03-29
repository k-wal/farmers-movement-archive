import re
import sys
import os
import requests
import json
import datetime
import numpy as np
import pickle
import twitter_image_script as image_script

params = {
    'key_identity': 'Xz9kFHaoaCaCKIz9Ez2UNjgBkLxLmZqg',
    'key_credential': 'dJsaJ18IZB25GYEwWzMadmT0G1CskF2y'
}

item_set_id = {
'11-2020' : 9314,
'08-2020' : 12266,
'10-2020' : 12327,
'09-2020' : 112431,
'12-2020' : 112506,
'01-2021' : 112574,
'02-2021' : 1331670,
'03-2021' : 1331671,
'04-2021' : 1331672
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
		"o:item_set" : [ {"o:id": item_set_id}, {"o:id" : 9315}], 
		"o:media" : []
	}

	response = requests.post('http://indiasocialarchive.iiit.ac.in/api/items', headers=headers, params=params, data=json.dumps(data))
	j = json.loads(response.text)
	return j['@id'].split('/')[-1]
	#print(j)

def upload_article_file(item_id, photo_path):
	headers = {
	'Content-Type': 'multipart/form-data'
	}


	data = {"o:ingester" : "upload", 
			"file_index" : "0", 
			"o:item" : {"o:id" : item_id}
			}

	files = [('data',(None, json.dumps(data), 'application/json')),
				('file[0]', (photo_path, open(photo_path, 'rb'), 'image/jpg'))]

	response = requests.post('http://indiasocialarchive.iiit.ac.in/api/media', params=params, files=files)
#	print(response)


def get_media_data(date, description, username, item_id):
	media_data = []
	url_in_tweet =  re.findall('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', description)

	if len(url_in_tweet) == 0:
		return []

	url_in_tweet = url_in_tweet[0]
	url_in_tweet = url_in_tweet[0]+'://'+url_in_tweet[1]+url_in_tweet[2]
	image_urls = image_script.get_image_url(url_in_tweet, date, username)

	if len(image_urls) > 0:
#		if len(image_urls) > 1:
#			print(image_urls)
		for image_url in image_urls:
			cur_data = {"o:ingester" : "url",
					"o:renderer" : "file",  
					"o:source" : image_url,
					"ingest_url" : image_url,
					"o:item" : {"o:id" : item_id}
					}
			media_data.append(cur_data)

	return media_data

def upload_file_url(date, item_id, description, username):
	headers = {
	'Content-Type': 'application/json'
	}

	media_data = get_media_data(date, description, username, item_id)

#	if len(media_data) > 1:
#		print(item_id)
	for data in media_data:
		response = requests.post('http://indiasocialarchive.iiit.ac.in/api/media', headers=headers ,params=params, data=json.dumps(data))

def if_upload(date, tweet_id):
	tweet_id = int(tweet_id)
	month = date.split('-')[1] + '-' + date.split('-')[0]
	
	dir_path = 'ids/' + month
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)

	dir_path = dir_path + '/' + date + '/'
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)

	filenames = os.listdir(dir_path)
	max_per_file = 1000

	cur_filepath = ''

	for filename in filenames:
		filepath = dir_path + filename

		with open(filepath, 'rb') as f:
			arr = pickle.load(f)

		if tweet_id in arr:
			return False

		if arr.size < max_per_file and cur_filepath == '':
			cur_filepath = filepath
		del arr

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
	del cur_arr
	return True

def upload_file(filepath, item_set_id):
	print("STARTING : " + filepath)
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()
	total = len(lines)
	for index, line in enumerate(lines):
		parts = line.split('|-|')
		try:
			date, tweet_id, username, text, url = parts[0].strip(), parts[1].strip(), parts[3].strip(), parts[7].strip(), parts[8].strip()
		except:
			continue
		if not if_upload(date,tweet_id):
			continue
		user_url = url.split('/status/')[0]
		if len(text) > 30:
			desc = text[0:30] + " . . . . "
		else:
			desc = text
		title = "<em>" + username + "</em> : " + desc

		# photo_path = image_script.if_image(text, date, username)
		item_id = upload_article(date, item_set_id, title, text, url, username, user_url, tweet_id)
		upload_file_url(date, item_id, text, username)
		# if photo_path != '':
		# 	upload_article_file(item_id, photo_path)
		# upload_article_url(date, item_set_id, title, text, url, username, user_url, tweet_id)

		if index % 10 == 0:
			print(str(index) + " of " + str(total) + " done")
	print("ENDING : " + filepath)


def upload_section(dir_path, item_set_id):
	filenames = os.listdir(dir_path)
	for filename in filenames:
		path = dir_path + '/' + filename
		print(filename + " : begin")
		upload_file(path, item_set_id)
		print(filename + " : end")

def write_hashtag_record(dir_path, hashtag, month):
	filepath = dir_path + '/' + month + '.txt'
	outfile = open(filepath, 'a')
	outfile.write(hashtag + '\n')
	outfile.close()

def if_already_uploaded(dir_path, hashtag, month):
	filepath = dir_path + '/' + month + '.txt'
	infile = open(filepath, 'r')
	lines = infile.readlines()
	infile.close()
	lines = [line.strip() for line in lines]
	if hashtag in lines:
		return True
	return False


tweet_dir_path = '../../corpus/tweets'
hashtags = os.listdir(tweet_dir_path)
month = '02-2021'

for hashtag in hashtags:
	if month+'.txt' not in os.listdir(tweet_dir_path+'/'+hashtag):
		continue
	filepath = tweet_dir_path + '/' + hashtag + '/' + month + '.txt'
	if if_already_uploaded('upload_records', hashtag, month):
		print("ALREADY DONE")
		continue
	upload_file(filepath, item_set_id[month])
	write_hashtag_record('upload_records', hashtag, month)
