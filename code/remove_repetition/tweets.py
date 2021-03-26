import os
import sys
import re
import pandas as pd
import numpy as np
import warnings

# get paths of all folders directly in directory given by dir_path
def get_folder_paths(dir_path):
	folder_names = os.listdir(dir_path)
	folder_paths = [dir_path + '/' + name for name in folder_names]
	return folder_paths

# get unique file names from all folder paths (filenames are month names : 08-2020.txt etc)
def get_file_names(folder_paths):
	filenames = []
	for path in folder_paths:
		filenames.extend(os.listdir(path))
	return list(set(filenames))

def get_month_dataframe(filename, folder_paths, output_dir):
	# creating main dataframe; check if theres a file for this month already
	if os.path.isfile(output_dir + '/' + filename):
		df = pd.read_csv(output_dir + '/' + filename, delimiter='\|\-\|', header=None, engine='python')
	else:
		df = pd.DataFrame(columns = list(range(10)))
	headers = list(range(10))
																			# going through each hashtag folder to find file and add to main dataframe
	for path in folder_paths:
		if filename not in os.listdir(path):
			continue
		hashtag = path.split('/')[-1] 																	#getting hashtag from path
		filepath = path + '/' + filename
		cur_df = pd.read_csv(filepath, delimiter='\|\-\|', header=None, engine='python')				#loading tweets for month for hashtag	
		cur_df[9] = [hashtag] * len(cur_df.index)														# adding new column for hashtag
		df = pd.concat([df, cur_df])																	# concatenating to main dataframe
	return df

def get_processed_month_dataframe(df, filename):
	new_df = pd.DataFrame(columns = list(range(10)))
	ids = df[1].unique()
	n_ids = len(ids)
	count = 0
	for cur_id in ids:
		rows = df.loc[df[1] == cur_id]
		hashtags = ','.join(rows[9].unique())
		hashtags = ','.join(list(set(hashtags.split(','))))
		new_row = rows.iloc[[0]]

		warnings.filterwarnings("ignore")
		new_row.iloc[0,9] = hashtags
		warnings.filterwarnings("default")
		
		# if ',' in hashtags:
		# 	print(new_row.iloc[0,9])

		new_df = pd.concat([new_df, new_row])
		
	#	indexNames = df[df[1] == cur_id].index
	#	df.drop(indexNames, inplace=True)
		
		count += 1
		if count%100 == 0:
			print(str(count) + "\t of " + str(n_ids) + ", filename = " + filename)
	return new_df

def write_new_file(df, output_dir, filename):
	np.savetxt(output_dir + '/' + filename, df, fmt='%s', delimiter = '|-|')


def main(dir_path, output_dir):
	paths = get_folder_paths(dir_path)
	filenames = get_file_names(paths)
	for filename in filenames:
		df = get_month_dataframe(filename, paths, output_dir)
		new_df = get_processed_month_dataframe(df, filename)
		write_new_file(new_df, output_dir, filename)		

dir_path = '../../corpus/tweets'
output_dir = '../../corpus/combined_tweets'
main(dir_path, output_dir)
