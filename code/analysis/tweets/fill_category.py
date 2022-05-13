import pandas as pd
import math

categories_df = pd.read_csv('classification.csv', lineterminator='\n')
categories_df.dropna(subset=['category'])
categories_df.drop(categories_df.columns.difference(['username','category']), 1, inplace=True)
print(categories_df)


bios_df = pd.read_csv('results/bios.txt', sep='\|\-\|', lineterminator='\n')
print(bios_df)
bios_df["category"] = None

for index in bios_df.index:
	username = bios_df.loc[index, 'username']

	temp_df = categories_df.loc[categories_df['username'] == username]
	for i,row in temp_df.iterrows():
		category = row['category']
		break
	if category:
		bios_df.loc[index, 'category'] = category

print(bios_df)
file = open("results/new_bios.txt",'w')
for index, row in bios_df.iterrows():
	username = row['username']
	if not isinstance(row['bio'], str):
		bio = ""
	else:
		bio = row['bio']
	if not isinstance(row['category'], str):
		category = ""
	else:
		category = row['category']
	
	try:
		to_write = '|-|'.join([username, bio, category, '\n'])
	except:
		bio = ''
		to_write = '|-|'.join([username, bio, category, '\n'])
	file.write(to_write)
file.close()
