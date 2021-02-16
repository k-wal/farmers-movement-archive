import os
import re


def get_hashtag_counts(dir_path, months):
	counts = []	
	for month in months:
		filepath = dir_path + '/' + month + '.txt'
		if not os.path.isfile(filepath):
			counts.append(0)
			continue
		file = open(filepath, 'r')
		lines = file.readlines()
		counts.append(len(lines))
		file.close()
	
	return counts



def write_to_file(dir_path, csv_filepath, md_filepath, months):
	n_months = len(months)
	csv_file = open(csv_filepath, 'w')
	md_file = open(md_filepath, 'w')

	header_md = '|' + 'HASHTAG' + '|' + '|'.join(months) + '|' + '\n'
	header_md += '|-----|' + '------|'*n_months + '\n'
	md_file.write(header_md)

	header_csv = 'HASHTAG' + ',' + ','.join(months) + '\n'
	csv_file.write(header_csv)

	hashtags = os.listdir(dir_path)
	
	for hashtag in hashtags:
		path = dir_path + '/' + hashtag
		counts = get_hashtag_counts(path, months)

		to_write_csv = hashtag + ',' + ','.join([str(count) for count in counts]) + '\n'
		to_write_md = '|' + hashtag + '|' + '|'.join([str(count) for count in counts]) + '|' + '\n'

		csv_file.write(to_write_csv)
		md_file.write(to_write_md)

	md_file.close()
	csv_file.close()


months = ['02-2021',
'01-2021',
'12-2020',
'11-2020',
'10-2020',
'09-2020',
'08-2020',
'07-2020',
'06-2020',
'05-2020',
'04-2020']

dir_path = '../corpus/tweets'
csv_filepath = '../doc/twitter_numbers.csv'
md_filepath = '../doc/twitter_numbers.md'

write_to_file(dir_path, csv_filepath, md_filepath, months)