import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
nlp = en_core_web_sm.load()

fixed_ents = [
'all india kisan sabha',
'all india kisan sangharsh coordination committee',
'samyukt kisan morcha',
'sanyukt kisan morcha',
'samyukta kisan morcha',
]

# fixed_ents = [
# 'All India Kisan Sabha',
# 'All India Kisan Sangharsh Coordination Committee',
# 'Samyukt Kisan Morcha',
# 'Sanyukt Kisan Morcha',
# 'Samyukta Kisan Morcha'
# ]

def make_ruler_patterns():
	patterns = []
	global fixed_ents
	for ent in fixed_ents:
		tokens = ent.split()
		pattern = {'label':'ORG', 'pattern':[]}
		for token in tokens:
			pattern['pattern'].append({"LOWER":token})
		patterns.append(pattern)
	return patterns

ruler = nlp.add_pipe("entity_ruler")
ruler.overwrite_ents = True
patterns = make_ruler_patterns()
ruler.add_patterns(patterns)


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


# return true if article is relevant, false otherwise
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

# get list of text from all relevant articles
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

# return list of ners from list of lines
def get_ner(lines):
	ners = []
	labels = ['PERSON', 'NORP', 'ORG']
	for line in lines:
		doc = nlp(line)
		# doc.ents = [X for X in doc.ents if X.label_ in labels]		# filtering to get only certain labels
		ners.append(doc)
	return ners

def print_ner(ners):
	pprint([(X.text, X.label_) for X in ners.ents])

def get_correct_ner(text):
	if text == 'bhartiya kisan union':
		return 'bku'
	if text == 'bharatiya kisan union':
		return 'bku'
	if text == 'bharatiya janata party':
		return 'bjp'
	if text == 'kisan mazdoor sangharsh committee':
		return 'kmsc'
	if text == 'u.p.':
		return 'uttar pradesh'
	if text == 'aam aadmi party':
		return 'aap'
	if text == 'ncp':
		return 'congress'
	if text == 'pm modi' or text == 'narendra modi' or text == 'prime minister':
		return 'modi'
	if text == 'all india kisan sabha':
		return 'aiks'
	if text == 'all india kisan sangharsh coordination committe':
		return 'aikscc'
	if text == 'samyukt kisan morcha' or text == 'sanyukt kisan morcha' or text == 'samyukta kisan morcha':
		return 'skm'

	# if text == 'all india':
	# 	return -1

	if 'akali' in text:
		return 'sad'
	if 'trinamool' in text:
		return 'tmc'
	if "'" in text:
		return text.split("'")[0]

	return text

def update_ner_counts(ners, counts, label_map):
	labels = ['PERSON', 'NORP', 'ORG']
	for line_ners in ners:
		for ner in line_ners.ents:
			ner_text, ner_label = ner.text.lower(), ner.label_
			if ner_text[0:4] == 'the ':
				ner_text = ner_text[4:]
			ner_text = get_correct_ner(ner_text)
			if ner_text == -1:
				continue
			if ner_label not in labels:
				continue
			if ner_text not in counts.keys():
				counts[ner_text] = 0
				label_map[ner_text] = ner_label
			counts[ner_text] += 1
	return counts, label_map


def get_month_ners(dir_path, ner_counts={}, label_map={}):
	print(dir_path)
	filenames = os.listdir(dir_path)
	for filename in filenames:
		filepath = dir_path + '/' + filename
		text = get_relevant_text(filepath)
		# print(text)
		ners = get_ner(text)
		ner_counts, label_map = update_ner_counts(ners, ner_counts, label_map)

	# sorting in descending order of frequency
	sorted_tuples = sorted(ner_counts.items(), key=lambda item: item[1], reverse=True)
	sorted_counts = {k: v for k, v in sorted_tuples}
	return sorted_counts, label_map

def get_all_ners(dir_path):
	ner_counts = {}
	label_map = {}

	for index, month in enumerate(os.listdir(dir_path)):
		print(index)
		if 'hindustantimes' in dir_path:
			ner_counts, label_map = get_month_ners(dir_path + '/' + month + '/combined', ner_counts, label_map)
		else:
			ner_counts, label_map = get_month_ners(dir_path + '/' + month, ner_counts, label_map)
		# print(ner_counts)
	sorted_tuples = sorted(ner_counts.items(), key=lambda item: item[1], reverse=True)
	sorted_counts = {k: v for k, v in sorted_tuples}
	return sorted_counts, label_map

def print_counts(counts, label_map,filename, limit):
	if len(counts.keys()) < limit:
		limit = len(counts.keys())	
	file = open('ner_lists/'+filename+'.txt','w')

	i = 0
	for entity in counts.keys():
		file.write(label_map[entity] + "||" + entity + "||" + str(counts[entity]) + "\n")
		i+=1
		if i==limit:
			break
	file.close()

def plot_wordcloud(counts):
	wordcloud = WordCloud(stopwords=stop_words, background_color="black", collocations=True)
	wordcloud.generate_from_frequencies(frequencies=counts)
	plt.figure(figsize=(8, 8))
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

dir_path = '../../../../corpus/hindu/01-2021'
filename = 'hindu-' + dir_path.split('/')[-1]

limit = 50
counts, label_map = get_month_ners(dir_path)
print_counts(counts, label_map, filename, limit)
plot_wordcloud(counts)

# dir_path = '../../../corpus/tribune/editorial'
# filename = 'tribune-editorial'

# dir_path = '../../../corpus/hindustantimes'
# filename = 'hindustan-times'

# dir_path = '../../../corpus/timesofindia'
# filename = 'timesofindia'

# dir_path = '../../../../corpus/hindu'
# filename = 'hindu'

# limit = 200
# counts, label_map = get_all_ners(dir_path)
# print_counts(counts, label_map, filename, limit)
# plot_wordcloud(counts)