#!/usr/bin/env python

import sys

changes		= {"CU10_12":"CU10.12", "CU10_17":"CU10.17","CU10_2":"CU10.2","CU10_7":"CU10.7","CU11_19":"CU11.19","CU11_7":"CU11.7","CU4_2":"CU4.2","CU6_1":"CU6.1","CU8_24":"CU8.24","CU8_3":"CU8.3"}

countries		= {"CU10.12":"Australia", "CU10.17":"Australia","CU10.2":"Australia","CU10.7":"Australia","CU11.19":"Australia","CU11.7":"Australia","CU4.2":"Australia","CU6.1":"Australia","CU8.24":"Australia","CU8.3":"Australia","S55":"USA","CULm":"Australia","CULa":"Australia","P314":"France","P163":"France","BloC104":"France","BloC014":"France","FrB5":"France","AB29":"Canada","321":"Canada","SK35":"Canada","MB21":"Canada","MB52":"Canada","Sssaf":"SouthAfrica","Ss44":"Morocco"}

colors		= {"CU10.12":"red", "CU10.17":"red","CU10.2":"red","CU10.7":"red","CU11.19":"red","CU11.7":"red","CU4.2":"red","CU6.1":"red","CU8.24":"red","CU8.3":"red","S55":"green","CULm":"red","CULa":"red","P314":"France","P163":"France","BloC104":"France","BloC014":"France","FrB5":"France","AB29":"black","321":"black","SK35":"black","MB21":"black","MB52":"black","Sssaf":"magenta","Ss44":"brown"}

file = open(sys.argv[1])
for line in file.readlines():
	fields	= line.split()
	if fields[0] in changes:
		fields[0]	= changes[fields[0]]
	if fields[1] in changes:
		fields[1]	= changes[fields[1]]
	if fields[2] != "99.0000":
		if countries[fields[0]] == "Australia" and countries[fields[1]] == "Australia":
			print "\t".join([fields[0], fields[1], fields[2], "red"])
		elif countries[fields[0]] == "Canada" and countries[fields[1]] == "Canada":
			print "\t".join([fields[0], fields[1], fields[2], "black"])
		elif countries[fields[0]] == "USA" and countries[fields[1]] == "USA":
			print "\t".join([fields[0], fields[1], fields[2], "green"])
		elif countries[fields[0]] == "SouthAfrica" and countries[fields[1]] == "SouthAfrica":
			print "\t".join([fields[0], fields[1], fields[2], "magenta"])
		elif countries[fields[0]] == "France" and countries[fields[1]] == "France":
			print "\t".join([fields[0], fields[1], fields[2], "blue"])
		elif countries[fields[0]] == "Morocco" and countries[fields[1]] == "Morocco":
			print "\t".join([fields[0], fields[1], fields[2], "brown"])
		else:
			print "\t".join([fields[0], fields[1], fields[2], "purple"])
	else:
			print "\t".join([fields[0], fields[1], fields[2], "grey"])
	

