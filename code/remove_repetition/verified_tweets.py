import pandas as pd
import os
import datetime

def get_file_dataframe(filepath):
	try:
		df = pd.read_csv(filepath, lineterminator='\n')
	except:
		df = pd.read_csv(filepath, lineterminator='\n', error_bad_lines=False)
		print(filepath)
	keeping_columns = ['id', 'date', 'tweet', 'hashtags', 'user_id', 'username', 'name', 'link', 'urls', 'nlikes', 'nretweets',
						'nreplies']
	df = df[keeping_columns]
	return df

def combine_date_tweets(dir_path, date):
	print(date.strftime("%d-%m-%Y"))
	date_string =  date.strftime("%Y-%m-%d")
	dir_path = dir_path + '/' + date_string
	date_df = pd.DataFrame()

	filenames = os.listdir(dir_path)
	for filename in filenames:
		filepath = dir_path + '/' + filename
		current_df = get_file_dataframe(filepath)
		date_df = pd.concat([date_df, current_df])
	
	date_df = date_df.drop_duplicates(subset = 'id')	# dropping duplicates based on id (incase a tweet has multiple relevant hashtags)
	filepath = dir_path + '/combined.csv'	#filepath for saving csv
	date_df.to_csv(filepath)


def main_func(dir_path, start_string, end_string):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	date = start_date
	while date <= end_date:
		combine_date_tweets(dir_path, date)

		date += datetime.timedelta(days=1)


start_string = '01-01-2021'
end_string = '28-02-2021'
dir_path = '../../corpus/verified_tweets'
main_func(dir_path, start_string, end_string)