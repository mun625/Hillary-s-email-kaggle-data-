# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
import math
from sentiment_score import WordDicToScore

def DeletePunctuation(word):
	my_word = word
	for c in ["'", ",", "°", "•", "`", '"', "‘", "-", "."]:
		my_word = my_word.replace(c, "")
	return my_word

def SentenceToWordList(sentence):
	sentence = str(sentence)
	word_list = re.split(' |[\r\n]+', sentence)								# split the sentence into words
	word_list = [DeletePunctuation(word.lower()) for word in word_list]		# delete punctuations which is unnecessary to analyze
	return word_list

def EmailsToWordDict(my_email):
	word_dic = {}
	for row in my_email.iterrows():
		for word in SentenceToWordList(row[1]['ExtractedBodyText']):
			word_dic.setdefault(word, 0)
			word_dic[word] += 1
	return word_dic

# Date format should be like 'XXXX-XX-XX' (e.g. '2010-06-25')
def SelectEmailsByDate(my_email, start_date, end_date):
	selection = np.where((my_email['MetadataDateSent'] >= start_date) & (my_email['MetadataDateSent'] <= end_date))
	if len(selection[0]) == 0:
		return []
	if len(selection[0]) == 1:
		return my_email.iloc[selection[0][0]:1]
	return my_email.iloc[selection[0][0]:selection[0][-1]]


emails = pd.read_csv("./output/Emails.csv")
sorted_emails = emails[['Id','DocNumber','MetadataDateSent','ExtractedDateSent','ExtractedBodyText']]
sorted_emails = sorted_emails.sort_values(by='MetadataDateSent', ascending=True)

emails2008 = SelectEmailsByDate(sorted_emails, '2008-01-01', '2008-12-31')
emails2009 = SelectEmailsByDate(sorted_emails, '2009-01-01', '2009-12-31')
emails2010 = SelectEmailsByDate(sorted_emails, '2010-01-01', '2010-12-31')
emails2011 = SelectEmailsByDate(sorted_emails, '2011-01-01', '2011-12-31')
emails2012 = SelectEmailsByDate(sorted_emails, '2012-01-01', '2012-12-31')
emails2013 = SelectEmailsByDate(sorted_emails, '2013-01-01', '2013-12-31')
emails2014 = SelectEmailsByDate(sorted_emails, '2014-01-01', '2014-12-31')

print "-----------------------Summary of Email contents-----------------------"
total = 0
num = 0
lastdate = ""
for row in sorted_emails.iterrows():
	total+=1
	if type(row[1]['MetadataDateSent']) != float:
		lastdate = row[1]['MetadataDateSent']
		num+=1
print "Total Number of Emails :", total
print "Number of emails that Datesent exists :", num
print "Start date of Email :", sorted_emails.iloc[0]['MetadataDateSent'][0:10]
print "Last date of Email :", lastdate[0:10], "\n"

print "Num of email sent on 2008 :", len(emails2008)
print "Num of email sent on 2009 :", len(emails2009)
print "Num of email sent on 2010 :", len(emails2010)
print "Num of email sent on 2011 :", len(emails2011)
print "Num of email sent on 2012 :", len(emails2012)
print "Num of email sent on 2013 :", len(emails2013)
print "Num of email sent on 2014 :", len(emails2014)
print "-----------------------------------------------------------------------", "\n"


print " 0. Sentiment Analysis"
word_dict = EmailsToWordDict(emails2012)
print WordDicToScore(word_dict)


print " 1. Word frequently used"
word_dict = EmailsToWordDict(sorted_emails)
useless_words = []
useless = open("./useless_word.txt")
for line in useless:
	useless_words.append(line.rstrip('\n'))
print len(useless_words)

#for key, value in sorted(word_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
#	if value > 20:
#		print "%s: %s" % (key, value)









