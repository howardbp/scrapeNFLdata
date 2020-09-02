import requests
from lxml import html
import csv

def week(playertype,weeknum):
	url = 'https://www.pro-football-reference.com/play-index/pgl_finder.cgi'
	resXpath = "//div[@id='div_results']/table[@id='results']/tbody/tr"
	headXpath = '//thead'

	params = {'age_max': '99',
		 'age_min': '0',
		 'c1comp': 'gt',
		 'c1val': '1',
		 'c2comp': 'gt',
		 'c3comp': 'gt',
		 'c4comp': 'gt',
		 'from_link': '1',
		 'game_num_max': '99',
		 'game_num_min': '0',
		 'game_type': 'A',
		 'match': 'game',
		 'request': '1',
		 'season_end': '-1',
		 'season_start': '1',
		 'week_num_max': str(weeknum),
		 'week_num_min': str(weeknum),
		 'year_max': '2019',
		 'year_min': '2019',
		 'offset':str(0)
	 }

	params['order_by'] = types[playertype][0]
	params['c1stat'] = types[playertype][1]
	allrows = list()

	i = 101
	while i >= 100:
		r = requests.get(url,params)
		page = html.fromstring(r.text)
		headers = [f.text for f in page.xpath(headXpath)[0][1]]
		if len(allrows) == 0:
			allrows.append(headers)
		
		results = [list(w.text_content() for w in k) for k in page.xpath(resXpath)]
		i = len([k for k in results if k != headers])
		params['offset'] = str(int(params['offset']) + 100)
		for player in results:
			if player[0].lower() != 'rk':
				allrows.append(player)
	return allrows


def getSeason(playertype):
	seasonStats = list()
	for i in range(1,17):
		wkstats = week(playertype,i)
		for row in wkstats:
			if row not in seasonStats:
				seasonStats.append(row)
	return seasonStats

types = {
	'wr':('rec_yds','rec'),
	'qb':('pass_rating','pass_att'),
	'rb':('rush_yds','rush_att'),
	'df':('sacks','tackles_solo')
}

for t in types:
	season = getSeason(t)
	with open(t + '.csv','wb') as outf:
		writer = csv.writer(outf)
		for row in season:
			writer.writerow(row)
