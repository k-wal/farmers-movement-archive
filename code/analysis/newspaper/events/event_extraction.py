import pandas as pd
import os
from pprint import pprint
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
import numpy as np
import spacy
from sklearn.cluster import DBSCAN
from tqdm import tqdm

np.random.seed(2018)

stemmer = SnowballStemmer('english')

# preprocessing text bit
def preprocess(text):
	result = []
	for token in gensim.utils.simple_preprocess(text):
		if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
			result.append(lemmatize_stemming(token))
	return result

# return True if one of the keywords is in the text
def is_keyword(text):
	keywords = [
		'farmer',
		'mandi',
		'agrarian crisis',
		'kisan sabha',
		'msp',
		'bku',
		'tikri', 
		'singhu', 
		'ghazipur',
		'anti-farmer',
		'agri-reform',
		'farm bill',
		'farm bills',
		'farmers bills',
		'farmers\' bills',
		'farm policy',
		'farm policies',
		'pro-farmer',
		'Essential Commodities (Amendment) Bill, 2020',
		'Essential Commodities Bill, 2020',
		'Essential Commodities Act, 2020',
		'agri bill',
		'agri ordinance',
		'farm ordinance',
		'trolley times',
		'Kisan Sangharsh Committee',
		'Kisan Bachao Morcha',
		'Kisan Mazdoor Sangharsh Committee',
		'Jai Kisan Andolan',
		'Punjab Kisan Union',
		'Kirti Kisan Union',
		'Terai Kisan Sangathan',
		'All India Kisan Sabha',
		'Mahila Kisan Adhikar Manch',
		'Doaba Kisan Samiti',
		'Rakesh Tikait',
		'Bhartiya Kisan Union']
	# print(text)

	for keyword in keywords:
		keyword = keyword.lower()
		if ' ' in keyword:
			if keyword in text.lower():
				return True
		else:
			regex = r'\b\w+\b'
			words = re.findall(regex, text.lower())
			if keyword in words:
				return True
	return False

# get dataframe from directory
def get_directory_df(dir_path):
	df = pd.DataFrame(columns=['date', 'title', 'text'])
	filenames = os.listdir(dir_path)
	filenames.sort()
	for filename in filenames:
		# print("reading : " + filename)
		filepath = dir_path + '/' + filename
		data = pd.read_csv(filepath, sep='\|\|', header=None, usecols=[2,3], names=['title', 'text'], engine='python')
		data = data.assign(date = filename.split('.')[0])
		df = df.append(data)
	return df

def filter_news_df(documents):
	documents['text'] = documents['text'].fillna('')
	documents['text'] = documents['text'].astype('string')

	documents['title'] = documents['title'].fillna('')
	documents['title'] = documents['title'].astype('string')

	documents['keywords_present'] = documents.apply(lambda row: is_keyword(row['text']), axis=1)
	documents = documents[documents['keywords_present'] == True]
	del documents['keywords_present']
	return documents

def get_vectors(df):
	model = spacy.load('en_core_web_lg')
	sent_vecs = {}
	docs = []
	for _,row in tqdm(df.iterrows(), total=df.shape[0]):
		title = row.title
		doc = model(title)
		docs.append(doc)
		sent_vecs.update({title: doc.vector})
	sentences = list(sent_vecs.keys())
	vectors = list(sent_vecs.values())
	return sentences, vectors

def get_clusters(sentences, vectors):
	x = np.array(vectors)
	n_classes = {}

	# for i in tqdm(np.arange(0.001, 1, 0.002)):
	# 	dbscan = DBSCAN(eps = i, min_samples = 2, metric = 'cosine').fit(x)
	# 	n_classes.update({i: len(pd.Series(dbscan.labels_).value_counts())})

	# for i in n_classes.keys():
	# 	print(i, n_classes[i])

	dbscan = DBSCAN(eps = 0.1, min_samples=2, metric='cosine').fit(x)
	labels = dbscan.labels_
	print("# CLUSTERS : " + str(len(pd.Series(labels).value_counts())))
	return dbscan


def show_dbscan_result(index, dbscan, sentences, df):
	results = pd.DataFrame({'label' : dbscan.labels_, 'sent' : sentences})
	example_result = results[results.label == index].sent.tolist()
	event_df = df[df.title.isin(example_result)][['date', 'title', 'newspaper']]
	event_df['date'] = pd.to_datetime(event_df.date, format="%d-%m-%Y", errors="ignore")
	event_df['date'] = pd.to_datetime(event_df.date, format="%B %-d, %Y", errors="ignore")
	event_df['date'] = pd.to_datetime(event_df.date, format="%d %B %Y", errors="ignore")
	event_df = event_df.sort_values(by='date').dropna()
	print(event_df)


def run_extraction(paths):
	df = pd.DataFrame(columns=['date', 'title', 'text', 'newspaper'])
	for newspaper in paths.keys():
		print("\n\n-------" + newspaper + "-------")
		dir_path = paths[newspaper]
		cur_df = get_directory_df(dir_path)
		filtered_df = filter_news_df(cur_df)
		filtered_df = filtered_df.assign(newspaper=newspaper)
		print("from " + newspaper + " : " + str(len(filtered_df.index)))
		df = pd.concat([filtered_df, df])
		print("current size : " + str(len(df.index)))

	sentences, vectors = get_vectors(df)
	dbscan = get_clusters(sentences, vectors)
	show_dbscan_result(10, dbscan, sentences, df)


month = '09-2020'
main_corpus_path = '../../../../corpus'
paths = {
'timesofindia' : main_corpus_path + '/timesofindia/' + month,
'hindustantimes' : main_corpus_path + '/hindustantimes/' + month + '/combined',
'hindu' : main_corpus_path + '/hindu/' + month,
'deccanherald' : main_corpus_path + '/deccanherald/' + month,
'telegraph' : main_corpus_path + '/telegraph/combined/' + month,
'tribune-punjab' : main_corpus_path + '/tribune/punjab/' + month,
'tribune-haryana' : main_corpus_path + '/tribune/haryana/' + month,
'tribune-nation' : main_corpus_path + '/tribune/nation/' + month
}
run_extraction(paths)