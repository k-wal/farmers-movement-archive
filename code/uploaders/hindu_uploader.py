from .upload_functions import UploadFunctions

class HinduUploader(UploadFunctions):

	def __init__(self):
		super(HinduUploader, self).__init__()
		self.hindu_item_set_id = 7347
		self.hindu_item_set_dict = {'12-2020' : 327,
		'11-2020' : 7348,
		'10-2020' : 7454,
		'09-2020' : 7972,
		'08-2020' : 8335,
		'07-2020' : 8495,
		'06-2020' : 9297,
		'05-2020' : 9298,
		'04-2020' : 9299,
		'01-2021' : 1319417,
		'02-2021' : 1324986,
		'03-2021' : 1325149,
		'04-2021' : 1325278,
		'05-2021' : 1331640,
		'06-2021' : 3439844,
		'07-2021' : 3439967,
		'08-2021' : 3439968,
		'09-2021' : 3441728,
		'10-2021' : 3443088,
		'11-2021' : 3443156,
		'12-2021' : 3444468}

		self.keywords = [
		# 'farmer',
		# 'mandi',
		# 'agrarian crisis',
		'kisan sabha',
		#'msp',
		'bku',
		'tikri', 
		'singhu', 
		# 'ghazipur',
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

	def get_location(self, part):
		if '--' in part:
			return ''
		if part[-1] == ',':
			return part[:-1]
		return part 

	def upload_date(self, date_string, filepath, month):
		self.upload_file(filepath, date_string, self.hindu_item_set_dict[month], 
			self.hindu_item_set_id,'The Hindu', '', self.keywords, self.get_location)

