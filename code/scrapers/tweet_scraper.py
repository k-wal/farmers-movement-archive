import twint
import os

def get_tweets_hashtag(ht, start_date, end_date, filepath):
	c = twint.Config()
	c.Search = "#" + ht
	c.Since = start_date
	c.Until = end_date
	# c.Location = True
	# c.Limit = 20
	c.Custom = 'CSV'
	c.Store_CSV = True
	c.Output = filepath
	c.Format = "{date} |-| {id} |-| {user_id} |-| {username} |-| {place} |-| {near} |-| {geo} |-| {tweet} |-| {link}"

	twint.run.Search(c)
	
def get_date_tweets_hashtag(hashtag, dates, dir_path):
	for d in dates:
		start_date, end_date, month = d[0], d[1], d[2]
		filepath = dir_path + '/' + month + '.txt'
		get_tweets_hashtag(hashtag, start_date, end_date, filepath)


date_files = [['2020-08-01','2020-08-31','08-2020'],
['2020-09-01','2020-09-30','09-2020'],
['2020-10-01','2020-10-31','10-2020'],
['2020-11-01','2020-11-30','11-2020'],
['2020-12-01','2020-12-31','12-2020'],
['2021-01-01','2021-01-31','01-2021'],
['2021-02-01','2021-02-09','02-2021']]

hashtags = ['FarmersStandingFirm',
'चक्काजाम_सफल_रहा',
'कृषि_कानून',
'किसान_आंदोलन',
'किसान_आंदोलन_जारी_रहेगा',
'भाग_मोदी_किसान_आया',
'NoFarmersNoFood',
'किसान_एकता_जिंदाबाद',
'अब_किसान_कमल_काटेगा',
'kisaanektazindabad',
'किसान',
'ValentinesWithFarmers']



for hashtag in hashtags:
	hashtag = hashtag.lower()
	dir_path = '../../corpus/tweets/' + hashtag
	
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)

	get_date_tweets_hashtag(hashtag, date_files, dir_path)


#filepath = '../corpus/tweets/' + hashtag + '/08-2020.txt'

#start_date = '2020-08-01'
#end_date = '2020-08-31'

#get_tweets_hashtag(hashtag, start_date, end_date, filepath)


