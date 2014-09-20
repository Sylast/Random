#!/usr/bin/python
import numpy as np
import sys
import os.path

#stringNetwork [word] [wordlist.txt]
def LevenNumber( word, target ):
	if word == target:
		return 0
	if word == 0:
		return len(target)
	if target == 0:
		return len(word)

	w = len(word)+1;
	t = len(target)+1;
	m = np.array([[0],[0]])
	m.resize( (w, t) )

	#Start matrix bounds to 1,2,3...
	#The word or its target can be reached by 
	#removing or adding chars
	for i in range(1, w):
		m[i,0] = i
	for j in range(1, t):
		m[0,j] = j
	#print m

	for j in range(1, t):
		for i in range(1, w):
			if word[i-1] == target[j-1]: 		#Letters are the same
				m[i,j] = m[i-1,j-1]		#No operation needed
			else:
				delet 	= m[i-1, j] + 1
				insert 	= m[i, j-1] + 1
				sub 	= m[i-1, j-1] + 1
				#Pick the smallest one
				m[i,j] = np.min( [delet, insert, sub] )

			#print m
	return m[len(word), len(target)]

def help():
	print
	print "stringNetwork [word] [wordlist.txt]"
	print "word -- the word that the network will be made for"
	print "wordlist.txt -- the file that has the population of words for the network"
	print


if len(sys.argv) < 3 or not os.path.exists(sys.argv[2]):
	help()
	exit()
word = sys.argv[1]
wordlist = open(sys.argv[2], 'r')

f = []		#Friends list
pff = []		#possible Friends of Friends
pfff = []		#possible Friends of Friends of Friends
ff = [[]]		#Friends' Friends
fff = [[[]]]	#Friends' Friends' Friends

for posFriend in wordlist:
	posFriend = posFriend.rstrip()
	LD = LevenNumber(word, posFriend)
	if LD == 1: f.append(posFriend)
	if LD == 2: pff.append(posFriend)
	if LD == 3: pfff.append(posFriend)


for i in range(0, len(f)):
	ff.append([]);
	fff.append([]);
	for j in range(0, len(pff)):
		if LevenNumber(f[i], pff[j]) == 1: ff[i].append(pff[j])
	
	for j in range(0, len(ff[i])):	
		fff[i].append([]);
		for k in range(0, len(pfff)):
			if LevenNumber(ff[i][j], pfff[k]) == 1: fff[i][j].append(pfff[k])

print "%s's Friends:" %word

for i in range(0,len(f)):
	print "\t" + f[i]
	for j in range(0, len(ff[i])):
		if ff[i][j] != "": print "\t\t" + ff[i][j]
		for k in range(0, len(fff[i][j])):
			if fff[i][j][k] != "": print "\t\t\t" + fff[i][j][k]
