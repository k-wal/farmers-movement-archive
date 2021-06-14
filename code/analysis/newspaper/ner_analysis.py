import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
nlp = en_core_web_sm.load()

stop_words = ["a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", 
"aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn",
"couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", 
"few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", 
"her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", 
"its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", 
"needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", 
"out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", 
"some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", 
"this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", 
"weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", 
"y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", 
"here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", 
"they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would"]


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

def get_relevant_text(filepath):
	file = open(filepath, 'r')
	lines = file.readlines()
	file.close()

	all_articles = []
	for line in lines:
		try:
			date, loc, title, desc, url = line.strip().split('||')
		except:
			continue
		if check_article_relevance(title, desc):
			all_articles.append(desc)
	return all_articles

def get_ner(lines):
	ners = []
	labels = ['PERSON', 'NORP', 'ORG']
	for line in lines:
		doc = nlp(line)
		doc.ents = [X for X in doc.ents if X.label_ in labels]		# filtering to get only certain labels
		ners.append(doc)
	return ners

def print_ner(ners):
	pprint([(X.text, X.label_) for X in ners.ents])

def update_ner_counts(ners, counts, label_map):
	for line_ners in ners:
		for ner in line_ners.ents:
			ner_text, ner_label = ner.text.lower(), ner.label_
			if ner_text not in counts.keys():
				counts[ner_text] = 0
				label_map[ner_text] = ner_label
			counts[ner_text] += 1
	return counts, label_map


def get_month_ners(dir_path, ner_counts, label_map):
	print(dir_path)
	filenames = os.listdir(dir_path)
	for filename in filenames:
		filepath = dir_path + '/' + filename
		text = get_relevant_text(filepath)
		# print(text)
		ners = get_ner(text)
		ner_counts, label_map = update_ner_counts(ners, ner_counts, label_map)
	return ner_counts, label_map
	# for ner in ners:
	# 	print_ner(ner)

def get_all_ners(dir_path):
	ner_counts = {}
	label_map = {}

	for month in os.listdir(dir_path):
		print(month)
		if 'hindustantimes' in dir_path:
			ner_counts, label_map = get_month_ners(dir_path + '/' + month + '/combined', ner_counts, label_map)
		else:
			ner_counts, label_map = get_month_ners(dir_path + '/' + month, ner_counts, label_map)
		# print(ner_counts)
	sorted_tuples = sorted(ner_counts.items(), key=lambda item: item[1], reverse=True)
	sorted_counts = {k: v for k, v in sorted_tuples}
	return sorted_counts, label_map

def print_counts(counts, label_map,filename):
	file = open('ner_results/'+filename+'.txt','w')
	for entity in counts.keys():
		file.write(label_map[entity] + "\t" + entity + "\t" + str(counts[entity]) + "\n")
	file.close()

def plot_wordcloud(counts):
	wordcloud = WordCloud(stopwords=stop_words, background_color="black", collocations=True)
	wordcloud.generate_from_frequencies(frequencies=counts)
	plt.figure(figsize=(8, 8))
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

# dir_path = '../../../corpus/tribune/editorial'
# filename = 'tribune-editorial'

dir_path = '../../../corpus/hindustantimes'
filename = 'hindustan-times'
counts, label_map = get_all_ners(dir_path)
print_counts(counts, label_map, filename)
plot_wordcloud(counts)