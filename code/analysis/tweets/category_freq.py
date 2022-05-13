import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np


def get_category_counts():
	categories_df = pd.read_csv('categories.csv', lineterminator='\n')
	categories_df.dropna(subset=['category'])
	categories_df.drop(categories_df.columns.difference(['username','category']), 1, inplace=True)

	counts_df = pd.read_csv('results/counts.txt', lineterminator='\n', sep='\|')

	category_counts = {}

	for index, row in categories_df.iterrows():
		category = row['category']
		if not isinstance(category, str):
			continue
		category = category.strip()
		username = row['username']
		
		temp_df = counts_df.loc[counts_df['username'] == username]
		for i,r in temp_df.iterrows():
			count = r['count']
			break

		if category not in category_counts.keys():
			category_counts[category] = 0
		category_counts[category] += count

	category_counts = {k: v for k, v in sorted(category_counts.items(), key=lambda item: item[1], reverse=True)}
	return category_counts


def plot_category_counts(category_counts):
	print(category_counts)
	n=7
	labels = []
	y = []
	for key in category_counts.keys():
		# if not key:
		# 	continue
		labels.append(key)
		y.append(category_counts[key])
	labels = labels[0:n]
	y = y[0:n]
	y = np.array(y)
	plt.pie(y, labels = labels)
	plt.show()

category_counts = get_category_counts()
plot_category_counts(category_counts)