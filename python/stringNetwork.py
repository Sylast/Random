#!/usr/bin/python
import numpy as np

def LevenNumber( s1, s2 ):
	if s1 == s2:
		return 0
	if len(s1) == 0:
		return len(s2)
	if len(s2) == 0:
		return len(s1)

	m = np.matrix()
	print m

LevenNumber("word", "words")
