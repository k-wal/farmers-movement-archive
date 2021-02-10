import twint


def get_tweets_hashtag(ht, start_date, end_date, filepath):
	c = twint.Config()
	c.Search = "#" + ht
	c.Since = start_date
	c.Until = end_date
	# c.Location = True
	# c.Limit = 20
	c.Custom = 'CSV'
	c.Store_CSV = True
	c.Output = filepath
	c.Format = "{date} |-| {id} |-| {user_id} |-| {username} |-| {place} |-| {near} |-| {geo} |-| {tweet} |-| {link}"

	twint.run.Search(c)
	


hashtag = 'farmersprotest'

filepath = '../corpus/tweets/' + hashtag + '/02-2021.txt'

start_date = '2021-02-01'
end_date = '2021-02-08'
get_tweets_hashtag(hashtag, start_date, end_date, filepath)


# year = '2020'
# month = '06'

# cur = 1
# end = 30
# while cur <= end:
# 	if cur < 10:
# 		str_cur = '0' + str(cur)
# 	else:
# 		str_cur = str(cur)
# 	start_date = year + '-' + month + '-' + str_cur

# 	cur += 1

# 	if cur < 10:
# 		str_cur = '0' + str(cur)
# 	else:
# 		str_cur = str(cur)
# 	end_date = year + '-' + month + '-' + str_cur

