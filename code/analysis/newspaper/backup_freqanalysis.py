from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

snowball = SnowballStemmer('english')

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
			parts = line.strip().split('||')
			title, desc = parts[2], parts[3]
		except:
			continue
		if check_article_relevance(title, desc):
			all_articles.append(desc)
	return all_articles


def preprocess_text(text):
	tokens = word_tokenize(text)
	words = [re.sub(r'[^\w\s]', '', token) for token in tokens]
	words = [word.lower() for word in words if word.isalpha()]
	words = [snowball.stem(word) for word in words if word not in stop_words]
	return words

def get_file_words(lines):
	all_words = []
	for line in lines:
		all_words.append(preprocess_text(line))
	return all_words

def update_word_counts(words, counts):
	for line_words in words:
		for word in line_words:
			if word not in counts.keys():
				counts[word] = 0
			counts[word] += 1
	return counts

def get_month_counts(dir_path, counts):
	print(dir_path)
	filenames = os.listdir(dir_path)
	for filename in filenames:
		filepath = dir_path + '/' + filename
		text = get_relevant_text(filepath)
		words = get_file_words(text)
		counts = update_word_counts(words, counts)
	return counts
	# for ner in ners:
	# 	print_ner(ner)

def get_all_counts(dir_path):
	counts = {}

	for index, month in enumerate(os.listdir(dir_path)):
		print(index)
		if 'hindustantimes' in dir_path:
			counts = get_month_counts(dir_path + '/' + month + '/combined', counts)
		else:
			counts = get_month_counts(dir_path + '/' + month, counts)
		# print(ner_counts)
	sorted_tuples = sorted(counts.items(), key=lambda item: item[1], reverse=True)
	sorted_counts = {k: v for k, v in sorted_tuples}
	return sorted_counts

def print_counts(counts, filename):
	file = open('freq_results/'+filename+'.txt','w')
	for entity in counts.keys():
		file.write(str(counts[entity]) + "\t" + entity + "\n")
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

# dir_path = '../../../corpus/hindustantimes'
# filename = 'hindustan-times'

# dir_path = '../../../corpus/timesofindia'
# filename = 'timesofindia'

dir_path = '../../../corpus/hindu'
filename = 'hindu'

counts = get_all_counts(dir_path)
print_counts(counts, filename)
plot_wordcloud(counts)