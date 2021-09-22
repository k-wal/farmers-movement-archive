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
		print("reading : " + filename)
		filepath = dir_path + '/' + filename
		data = pd.read_csv(filepath, sep='\|\|', header=None, usecols=[0, 2,3], names=['date', 'title', 'text'])
		df = df.append(data)
	return df

def filter_news_df(documents):
	documents['text'] = documents['text'].fillna('')
	documents['text'] = documents['text'].astype('string')

	documents['title'] = documents['title'].fillna('')
	documents['title'] = documents['title'].astype('string')

	documents['keywords_present'] = documents.apply(lambda row: is_keyword(row['text']), axis=1)
	documents = documents[documents['keywords_present'] == True]
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

	# for i in tqdm(np.arrange(0.001, 1, 0.002)):
	# 	dbscan = DBSCAN(eps = i, min_samples = 2, metric = 'cosine').fit(x)
	# 	n_classes.update({i: len(pd.series(dbscan.labels_).value_counts())})

	dbscan = DBSCAN(eps = 20, min_samples=10, metric='cosine').fit(x)
	labels = dbscan.labels_
	print("# CLUSTERS : " + str(len(labels)))

	# results = pd.DataFrame({'label' : dbscan.labels_, 'sent' : sentences})

def run_extraction(dir_path):
	df = get_directory_df(dir_path)
	filtered_df = filter_news_df(df)
	sentences, vectors = get_vectors(filtered_df)
	get_clusters(sentences, vectors)

dir_path = '../../../../corpus/timesofindia/09-2020'
run_extraction(dir_path)