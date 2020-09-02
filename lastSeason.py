import csv
import pandas as pd

def tryF(strin):
	try:
		return float(strin)
	except:
		return strin

def rbPoints(playerIn):
	ptWeights = {
		'RushingYDs':.1,
		'RushingTD':6,
		'Rec':1,
		'ReceivingYDs':.1,
		'ReceivingTD':6,
		'FL':-2
	}

	relStats = {k:playerIn[k] for k in playerIn if k in ptWeights}
	playerIn['weightedPoints'] = round(sum(ptWeights[f] * relStats[f] for f in relStats),2)
	playerIn['ppg'] = round(playerIn['weightedPoints'] / playerIn['G'],2)
	return playerIn

def pDat(fin):
	with open(fin,'rb') as inf:
		dat = list(csv.reader(inf))

	dat = [list(tryF(dp) for dp in s) for s in dat]
	headers = dat[0]
	h = {k:1 for k in set(headers)}
	for e,i in enumerate(headers):
		if h[i] > 1:
			i = i + '.' + str(h[i] - 1)
			headers[e] = i
		h[i.split('.')[0]] += 1

	rn = {
		'TD': 'PassingTD',
		'TD.1': 'RushingTD',
		'TD.2': 'ReceivingTD',
		'TD.3': 'TotalTD',
		'Yds': 'PassingYDs',
		'Yds.1': 'RushingYDs',
		'Yds.2': 'ReceivingYDs',
		'Att': 'PassingAtt',
		'Att.1': 'RushingAtt'
	}
	headers = [rn.get(f,f) for f in dat[0]]

	return [dict(zip(headers,k)) for k in dat[1:]]

def isoPosition(posin,allPlayers):
	return [k for k in allPlayers if k['FantPos'] == posin]


s = pDat('2019.csv')
rbs = map(rbPoints,isoPosition('RB',s))
