import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def get_date_tweets(dir_path, date):
	date_string =  date.strftime("%Y-%m-%d")
	filepath = dir_path + '/' + date_string + '/combined.csv'
	df = pd.read_csv(filepath, lineterminator='\n')
	return df

def get_interval_tweets(start_string, end_string, dir_path):
	start_date = datetime.datetime.strptime(start_string, "%d-%m-%Y")
	end_date = datetime.datetime.strptime(end_string, "%d-%m-%Y")
	
	interval_df = pd.DataFrame()
	date = start_date
	while date <= end_date:
		cur_df = get_date_tweets(dir_path, date)
		interval_df = pd.concat([interval_df, cur_df])

		date += datetime.timedelta(days=1)

	return interval_df

def get_user_frequency(df):
	print(len(df))
	df['freq'] = df.groupby('username')['username'].transform('count')
	freq = df['username'].value_counts()
	return df, freq

# plot the wordcloud with given counts
def plot_wordcloud(counts, filename=''):
	wordcloud = WordCloud(background_color="black", collocations=True)
	wordcloud.generate_from_frequencies(frequencies=counts)
	plt.figure(figsize=(8, 8))
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	# plt.savefig(filename + '.png')
	plt.show()
	plt.close()

def plot_frequency_graph(counts):
	n=20
	counts = counts.to_dict()
	keys = [k for k in counts.keys()]
	values = [counts[k] for k in keys]
	plt.rcParams['font.size'] = '8'
	plt.xticks(rotation='vertical')
	plt.bar(keys[0:n], values[0:n], 0.6)
	plt.show()

def plot_freq(freq):
	print(type(freq))
	plot_frequency_graph(freq)
	# plot_wordcloud(freq)

def create_directory(dir_path):
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
	return

def print_freq(freq, start_string, end_string):
	dir_path = 'results'
	create_directory(dir_path)
	filepath = dir_path + '/' + start_string + '_' + end_string + '.txt'
	file = open(filepath, 'w')
	for user in freq.keys():
		to_write = user + '|' + str(freq[user]) + '\n'
		file.write(to_write)
	file.close()

def main_func(start_string, end_string, dir_path):
	df = get_interval_tweets(start_string, end_string, dir_path)
	df, freq = get_user_frequency(df)
	print_freq(freq, start_string, end_string)	
	# plot_freq(freq)

start_string = '01-01-2021'
end_string = '28-02-2021'
dir_path = '../../../corpus/verified_tweets'

main_func(start_string, end_string, dir_path)