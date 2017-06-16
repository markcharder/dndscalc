#!/usr/bin/env python

import warnings
import argparse
import re
from Bio.Seq import Seq
from Bio import SeqIO

parser	= argparse.ArgumentParser()

parser.add_argument(	'-a',
			dest='gff',
			metavar='GFF',
			help='Gff file containing only CDS sequences'	)
parser.add_argument(	'-b',
			dest='fasta',
			metavar='FASTA',
			help='Fasta file containing sequences from cds intervals modified by fastaAlternateReferenceMaker.'	)
parser.add_argument(	'-c',
			dest='output',
			metavar='OUTPUT',
			help='Output file prefix. Defaults to "out"',
			default='out'	)

options	= parser.parse_args()

if not options.gff or not options.fasta:
	parser.error("Please specify input files.")

count		= 1
cdsorder	= dict()
cdsstrands	= dict()
file		= open(options.gff, 'r')
for line in file.readlines():
	if not re.match('#', line):
		fields	= line.split()
		name	= fields[8].split(';')[0][3:]
		name	= name.split('.')
		name	= name[2]
		if name not in cdsorder:
			cdsorder[name]	= [count]
		else:
			cdsorder[name].append(count)
		count	+= 1
		cdsstrands[name]	= fields[6]

file.close()

count		= 0
fastaorder	= dict()
file		= open(options.fasta, 'r')
for line in file.readlines():
	if re.match('>', line):
		count	+= 1
		fastaorder[count] = []
	else:
		fastaorder[count].append(line[:-1])
file.close()
print cdsorder
print fastaorder
sequences	= dict()
proteins	= dict()

with warnings.catch_warnings():
#	warnings.simplefilter("ignore")
	for key, value in cdsorder.iteritems():
		concatenated	= list()
		for i in range(0,len(value)):
			if value[i] in fastaorder:
				concatenated	= concatenated + fastaorder[value[i]]
		concatenated	= ''.join(concatenated)
		concatenated	= Seq(concatenated)
		if str(cdsstrands[key]) == "-":
			concatenated	= concatenated.reverse_complement()
		sequences[key]	= concatenated
		proteins[key]	= concatenated.translate()
		concatenated	= list()


with open(options.output + '.cds.fa', 'w') as outfile:
	for key, value in sequences.iteritems():
		string	= '>' + key + '_strand:' + str(cdsstrands[key]) + '\n' + str(sequences[key]) + '\n'
		outfile.write(string)

with open(options.output + '.pep.fa', 'w') as outfile:
	for key, value in proteins.iteritems():
		string	= '>' + key + '_strand:' + str(cdsstrands[key]) + '\n' + str(proteins[key]) + '\n'
		outfile.write(string)

