import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

stemmer = SnowballStemmer('english')

to_exclude = [
"farmer",
"farm",
"protest",
"law",
"state",
"leader",
"govern",
"delhi",
"border",
"singh",
"polic",
"union",
"punjab",
"kisan",
"parti",
"day",
"continu",
"new",
"support",
"minist",
"centr",
"talk",
"sit",
"haryana"]
STOPWORDS = list(STOPWORDS)
STOPWORDS.extend(to_exclude)

def check_article_relevance(title, desc):
	keywords = [
	'kisan sabha',
	'bku',
	'tikri', 
	'singhu', 
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

	title = title.lower()
	desc = desc.lower()
	for keyword in keywords:
		keyword = keyword.lower()
		if keyword in title or keyword in desc:
			return True
	return False

def get_relevant_text(article_df, filepath):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()

	for line in lines:
		try:
			parts = line.strip().split('||')
			title, desc = parts[2], parts[3]
		except:
			continue
		if check_article_relevance(title, desc):
			cur_df = pd.DataFrame({"text":[desc]})
			article_df = article_df.append(cur_df, ignore_index = True)
	return article_df


def lemmatize_stemming(text):
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def preprocess_text(text):
	result = []
	for token in gensim.utils.simple_preprocess(text):
		if token not in STOPWORDS and len(token) >= 3:
			token = lemmatize_stemming(token)
			if token not in STOPWORDS:
				result.append(token)
	return result

def get_month_articles(dir_path, article_df):
	print(dir_path)
	filenames = os.listdir(dir_path)
	for filename in filenames:
		filepath = dir_path + '/' + filename
		article_df = get_relevant_text(article_df, filepath)
	return article_df
	# for ner in ners:
	# 	print_ner(ner)

def get_counts(df):
	dictionary = gensim.corpora.Dictionary(df)
	dictionary.filter_extremes(no_below=200, no_above=1, keep_n=200)
	vocab = list(dictionary.values()) #list of terms in the dictionary
	
	corpus = [dictionary.doc2bow(sent) for sent in df]
	vocab_tf={}
	for i in corpus:
		for item,count in dict(i).items():
			if item in vocab_tf:
				vocab_tf[item]+=count
			else:
				vocab_tf[item] = count

	global to_exclude
	counts = {}
	for i, word in enumerate(vocab):
		counts[word] = vocab_tf[i]
	return counts

def get_all_counts(dir_path):
	article_df = pd.DataFrame({"text":[]})

	for index, month in enumerate(os.listdir(dir_path)):
		print(index)
		if 'hindustantimes' in dir_path:
			article_df = get_month_articles(dir_path + '/' + month + '/combined', article_df)
		else:
			article_df = get_month_articles(dir_path + '/' + month, article_df)
		# print(ner_counts)
	processed_df = article_df['text'].map(preprocess_text)
	counts = get_counts(processed_df)
	return counts

def print_counts(counts, filename):
	file = open('freq_results/'+filename+'.txt','w')
	for entity in counts.keys():
		file.write(str(counts[entity]) + "\t" + entity + "\n")
	file.close()

def plot_wordcloud(counts):
	wordcloud = WordCloud(stopwords=STOPWORDS, background_color="black", collocations=True)
	wordcloud.generate_from_frequencies(frequencies=counts)
	plt.figure(figsize=(8, 8))
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

# dir_path = '../../../corpus/tribune/punjab'
# filename = 'tribune-punjab'

# dir_path = '../../../corpus/tribune/nation'
# filename = 'tribune-nation'

# dir_path = '../../../corpus/hindustantimes'
# filename = 'hindustan-times'

# dir_path = '../../../corpus/timesofindia'
# filename = 'timesofindia'

dir_path = '../../../corpus/hindu'
filename = 'hindu'

counts = get_all_counts(dir_path)
print_counts(counts, filename)
plot_wordcloud(counts)