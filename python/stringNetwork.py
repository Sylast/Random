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

	m = np.array([[0],[0]])
	m.resize( (len(word), len(target)) )

	#Start matrix bounds to 1,2,3...
	#The word or its target can be reached by 
	#removing or adding chars
	for i in range(1, len(word)):
		m[i,0] = i
	for j in range(1, len(target)):
		m[0,j] = j
	#print m

	for j in range(1,len(target)):
		for i in range(1,len(word)):
			if word[i] == target[j]: 		#Letters are the same
				m[i,j] = m[i-1,j-1]		#No operation needed
			else:
				delet 	= m[i-1, j] + 1
				insert 	= m[i, j-1] + 1
				sub 	= m[i-1, j-1] + 1
				#Pick the smallest one
				m[i,j] = np.min( [delet, insert, sub] )

			#print m
	return m[len(word)-1, len(target)-1]

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

fnetwork = []
ffnetwork = [[],[]]
fffnetwork = [[],[],[]]
f 	= 0
ff	= 0
fff	= 0 

for ftarget in wordlist:
	if LevenNumber(word, ftarget) == 1:
		print ftarget
		fnetwork.append(ftarget)
		#for fftarget in wordlist:
		#	if LevenNumber(word, fftarget) == 1:
		#		ffnetwork.append(fftarget)
		#		for ffftarget in wordlist:
		#			if LevenNumber(word, ffftarget) == 1:
		#				fffnetwork.append(ffftarget)
	
print "%s's Friends:" %word
print fnetwork 
print ffnetwork
print fffnetwork
