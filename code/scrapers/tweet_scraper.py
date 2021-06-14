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


date_files = [['2021-02-10','2021-02-28','02-2021'],
['2021-03-01','2021-03-31','03-2021'],
['2021-04-01','2021-04-30','04-2021'],
['2021-05-01','2021-05-31','05-2021']]

def get_hashtags():
	f = open('hashtags.txt','r')
	lines = f.readlines()
	f.close()
	hashtags = [line.strip() for line in lines]
	return hashtags

hashtags = get_hashtags()
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


