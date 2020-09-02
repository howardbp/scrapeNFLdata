def tryF(strin):
	try:
		return float(strin)
	except:
		return strin

def pDat(fin):
	with open(fin,'rb') as inf:
		dat = list(csv.reader(inf))

	dat = [list(tryF(dp) for dp in s) for s in dat]
	return dat[0],dat[1:]

def std(stats):
	rbs = {k:[] for k in set(f[1] for f in stats)}
	for player in stats:
		rbs[player[1]].append(player[14])

	describe = list()
	for e in rbs:
		allyards = rbs[e]
		gamesPlayed = len(allyards)
		averageYardsPerGame = round(sum(allyards) / gamesPlayed,2)
		variance = sum([((x - averageYardsPerGame) ** 2) for x in allyards]) / gamesPlayed
		std = round(variance ** .5,2)
		describe.append([ e,gamesPlayed,averageYardsPerGame,std])
	return describe

headers,stats = pDat('rb.csv')
b = std(stats)
