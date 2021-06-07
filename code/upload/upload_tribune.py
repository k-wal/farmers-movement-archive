from .upload_functions import *
import shutil
import os

def get_location(part):
	if '--' in part:
		return ''
	if ' ' in part and part!='New Delhi':
		return ''
	return part 

def move_files(source_dir, target_dir):
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)

	file_names = os.listdir(source_dir)
	    
	for file_name in file_names:
	    shutil.move(os.path.join(source_dir, file_name), target_dir)	


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

item_set_dict = {'nation' : 330,
'delhi' : 326,
'punjab' : 324,
'haryana' : 325,
'editorial' : 328,
'chandigarh': 333,
'bathinda': 332,
'amritsar' : 331,
'jalandhar' : 334,
'feature' : 329,
'comment' : 1328588,
'musing' : 1328589,
'business' : 1328590,
'ludhiana' : 1328591,
'patiala' : 1328592,
'himachalpradesh' : 1328593,
'jammukashmir' : 1328595
}
tribune_item_set_id = 323

def upload_move_section(section_name, path):
	dir_path = path + '/' + section_name
	# dir_path = '../../corpus/tribune/punjab'
	months = sorted(os.listdir(dir_path))
	for month in months:
		cur_dir_path = dir_path + '/' + month
		upload_section(cur_dir_path, item_set_dict[section_name], tribune_item_set_id,'The Tribune', '', keywords, get_location)
		move_files(cur_dir_path, '../../corpus/tribune/' + section_name + '/' + month)