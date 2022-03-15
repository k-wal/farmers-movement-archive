import twint
import os
import datetime

# store tweets with hashtag ht in the given interval in filepath
def get_tweets_hashtag(ht, start_date, end_date, filepath):
	print(start_date, ht)
	c = twint.Config()
	c.Search = ht
	c.Since = start_date
	c.Until = end_date
	c.Verified = True
	c.Stats = True
	# c.Min_likes = 20
	# c.Min_retweets = 5
	# c.Min_replies = 10
	
	# c.Custom = 'CSV'
	# config_format = '{id}|-|{datestamp}|-|{user_id}|-|{username}|-|{name}|-|{tweet}|-|{urls}|-|'
	# config_format += '{replies_count}|-|{retweets_count}|-|{likes_count}|-|{hashtags}|-|{link}'
	# c.Format = config_format
	# c.Store_CSV = True
	
	# c.Custom_csv = ["id", "user_id", "username", "tweet", "urls", "replies_count", "retweets_count", "likes_count", "link"]
	c.Pandas = True

	twint.run.Search(c)
	df = twint.storage.panda.Tweets_df
	if len(df) > 0:
		df.to_csv(filepath)
	
# create directory if not already created
def create_directory(dir_path):
	if os.path.isdir(dir_path):
		return
	os.makedirs(dir_path)

# get all tweets for a particular hashtag in a given interval
def get_date_tweets_hashtag(hashtag, start_string, end_string, dir_path):
	start_date = datetime.datetime.strptime(start_string, "%Y-%m-%d")
	end_date = datetime.datetime.strptime(end_string, "%Y-%m-%d")
	
	date = start_date
	while date <= end_date:
		date_string =  date.strftime("%Y-%m-%d")
		month_string = date.strftime("%Y-%m")
		next_date = date + datetime.timedelta(days=1)
		next_date_string = next_date.strftime("%Y-%m-%d")
		cur_dir_path = dir_path + '/' + month_string + '/' + date_string
		create_directory(cur_dir_path)
		filepath = cur_dir_path + '/' + hashtag + '.csv'
		get_tweets_hashtag(hashtag, date_string, next_date_string, filepath)

		date += datetime.timedelta(days=1)


def get_keywords():
	keywords = [
	'farmers protest',
	'kisan andolan'
	]
	return keywords

# get hashtags from hashtags file
def get_hashtags():
	f = open('hashtags.txt','r')
	lines = f.readlines()
	f.close()
	hashtags = ['#'+line.strip() for line in lines]
	
	keywords = get_keywords()
	hashtags.extend(keywords)
	
	return hashtags

# get tweets from all hashtags from a particular date
def get_all_tweets_date(date, dir_path):
	hashtags = get_hashtags()
	for hashtag in hashtags:
		date_string =  date.strftime("%Y-%m-%d")
		month_string = date.strftime("%Y-%m")
		next_date = date + datetime.timedelta(days=1)
		next_date_string = next_date.strftime("%Y-%m-%d")
		cur_dir_path = dir_path + '/' + month_string + '/' + date_string
		create_directory(cur_dir_path)
		filepath = cur_dir_path + '/' + hashtag + '.csv'
		get_tweets_hashtag(hashtag, date_string, next_date_string, filepath)

# main function, to scrape and store tweets from an interval that have all relevant hashtags
def main_func(start_string, end_string, dir_path):
	create_directory(dir_path)
	start_date = datetime.datetime.strptime(start_string, "%Y-%m-%d")
	end_date = datetime.datetime.strptime(end_string, "%Y-%m-%d")
	
	date = start_date
	while date <= end_date:
		get_all_tweets_date(date, dir_path)
		date += datetime.timedelta(days=1)

start_string = '2022-02-01'
end_string = '2022-02-28'
dir_path = '../../corpus/verified_tweets'
main_func(start_string, end_string, dir_path)

# start_string = '2021-01-01'
# end_string = '2021-01-25'
# hashtags = get_hashtags()
# for hashtag in hashtags:
# 	hashtag = hashtag.lower()
# 	dir_path = '../../corpus/verified_tweets'
	
# 	if not os.path.isdir(dir_path):
# 		os.mkdir(dir_path)

# 	get_date_tweets_hashtag(hashtag, start_string, end_string, dir_path)
