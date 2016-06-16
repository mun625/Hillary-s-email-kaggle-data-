import json

def ScoreDic(fp):
	score_file = open(fp)	# open the score file
	score_dic = {}			# initialize an empty dictionary
	for line in score_file:
		term, score = line.split("\t")	# the file is tab-deliminated.
		score_dic[term] = int(score)	# Convert the score to an integer.
	return score_dic

def WordDicToScore(word_dic, score_dic = ScoreDic('AFINN-111.txt')):
	score = 0
	for key, value in word_dic.iteritems():
		if key in score_dic.keys():
			score += score_dic[key]*value
	return score

