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
np.random.seed(2018)

stemmer = SnowballStemmer('english')

# lemmatizing and stemming
def lemmatize_stemming(text):
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

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
	df = pd.DataFrame(columns=['title'])
	for filename in os.listdir(dir_path):
		print("reading : " + filename)
		filepath = dir_path + '/' + filename
		data = pd.read_csv(filepath, sep='\|\|', header=None, usecols=[2,3], names=['title', 'text'])
		df = df.append(data)
	return df

def get_bow_corpus_tfidf(documents, apply_keywords=True):
	if apply_keywords:
		documents['text'] = documents['text'].fillna('')
		documents['text'] = documents['text'].astype('string')
		documents['keywords_present'] = documents.apply(lambda row: is_keyword(row['text']), axis=1)
		documents = documents[documents['keywords_present'] == True]
	
	print(documents)
	processed_docs = documents['text'].fillna('').map(preprocess)
	dictionary = gensim.corpora.Dictionary(processed_docs)
	count = 0
	dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=10000)
	bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
	tfidf = models.TfidfModel(bow_corpus)
	corpus_tfidf = tfidf[bow_corpus]
	
	return bow_corpus, corpus_tfidf, dictionary
	# for doc in corpus_tfidf:
	#	 pprint(doc)
 #		break	

# run LDA using bag-of-words
def run_lda_bow(bow_corpus, dictionary):
	lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=20, id2word=dictionary, passes=2, workers=2)
	for idx, topic in lda_model.print_topics(-1):
		# if 'farmer' in topic or 'farm' in topic or 'agri' in topic:
		# 	print('Topic: {} Words: {}'.format(idx, topic))
		print('Topic: {} Words: {}'.format(idx, topic))

# run LDA using TF-IDF method
def run_lda_tfidf(corpus_tfidf, dictionary):
	lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=20, id2word=dictionary, passes=20, workers=4)
	for idx, topic in lda_model_tfidf.print_topics(-1):
		# if 'farmer' in topic or 'farm' in topic or 'agri' in topic:
		# 	print('Topic: {} Words: {}'.format(idx, topic))
		print('Topic: {} Words: {}'.format(idx, topic))

def run_lda(documents):
	bow_corpus, corpus_tfidf, dictionary = get_bow_corpus_tfidf(documents)
	# run_lda_bow(bow_corpus, dictionary)
	run_lda_tfidf(corpus_tfidf, dictionary)

# dir_path = '../../../../corpus/hindu/09-2020'
# dir_path = '../../../../corpus/tribune/punjab/09-2020'
dir_path = '../../../../corpus/timesofindia/09-2020'
documents = get_directory_df(dir_path)
run_lda(documents)