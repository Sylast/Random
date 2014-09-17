#!/usr/bin/python
import numpy as np
import sys

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

#file word.txt = open(argv[1], 'r')
#wordList = [sys.argv[0]]

