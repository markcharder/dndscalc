#!/usr/bin/env python

import argparse
import re

parser	= argparse.ArgumentParser()

parser.add_argument(	'-a',
			dest='gff',
			metavar='GFF',
			help='Gff file to adjust.'	)
parser.add_argument(	'-b',
			dest='vcf',
			metavar='VCF',
			help='Vcf file to inform adjustment of gff.'	)
parser.add_argument(	'-c',
			dest='prefix',
			metavar='PREFIX',
			help='Prefix of output files. Defaults to "out".',
			default='out'	)

options	= parser.parse_args()

if not options.gff or not options.vcf:
	parser.error("Please specify input files")

exons		= dict()
cdss		= dict()
genes		= dict()
mrnas		= dict()
chromosomes	= dict()
strands		= dict()
sources		= dict()
phases		= dict()
cdsstrands	= dict()
cdssources	= dict()
cdsphases	= dict()
exonstrands	= dict()
exonsources	= dict()
exonphases	= dict()

print "Reading gff..."
gff	= open(options.gff, 'r')
for line in gff.readlines():
	fields		= line.split()
	if fields[2] == "gene":
		name			= fields[8].split(";")[0][3:]
		genes[name]		= [fields[3], fields[4]]
		strands[name]		= fields[6]
		chromosomes[name]	= fields[0]
		sources[name]		= fields[5]
		phases[name]		= fields[7]
	if fields[2] == "mRNA":
		mrnas[name]	= [fields[3], fields[4]]
	if fields[2] == "exon":
		if name not in exons:
			exons[name]		= [[fields[3], fields[4]]]
			exonstrands[name]	= [fields[6]]
			exonsources[name]	= [fields[5]]
			exonphases[name]	= [fields[7]]
		else:
			exons[name].append([fields[3], fields[4]])
			exonstrands[name].append(fields[6])
			exonsources[name].append(fields[5])
			exonphases[name].append(fields[7])
	if fields[2] == "CDS":
		if name not in cdss:
			cdss[name]	= [[fields[3], fields[4]]]
			cdsstrands[name]	= [fields[6]]
			cdssources[name]	= [fields[5]]
			cdsphases[name]	= [fields[7]]
		else:
			cdss[name].append([fields[3], fields[4]])
			cdsstrands[name].append(fields[6])
			cdssources[name].append(fields[5])
			cdsphases[name].append(fields[7])
gff.close()
print "Done"

positions	= dict()
references	= dict()
alternates	= dict()
additions	= dict()

print "Reading vcf..."
vcf		= open(options.vcf, 'r')
for line in vcf.readlines():
	if not re.match("^#", line):
		fields	= line.split()
		if fields[6] == "PASS":
			if len(fields[4]) > len(fields[3]):
				addition	= (len(fields[4]) - 1)
			elif len(fields[4]) < len(fields[3]):
				addition	= -(len(fields[3]) - 1)
			else:
				addition	= 0
			if fields[0] not in positions:
				positions[fields[0]]	= [fields[1]]
				references[fields[0]]	= [fields[3]]
				alternates[fields[0]]	= [fields[4]]
				additions[fields[0]]	= [addition]
			else:
				positions[fields[0]].append(fields[1])
				references[fields[0]].append(fields[3])
				alternates[fields[0]].append(fields[4])
				additions[fields[0]].append(addition)

print "Done"

print "Fixing gff..."
for key, value in positions.iteritems():
	for i in range(0, len(value)):
#		print key, value[i], additions[key][i], references[key][i], alternates[key][i], positions[key][i]
		for ikey, ivalue in genes.iteritems():
			if chromosomes[ikey] == key:
				for n in range(0, len(ivalue)):
					if int(ivalue[n]) > int(value[i]):
						genes[ikey][n]	= int(genes[ikey][n]) + additions[key][i]
						mrnas[ikey][n]	= int(genes[ikey][n]) + additions[key][i]
		for ikey, ivalue in cdss.iteritems():
			if chromosomes[ikey] == key:
				for n in range(0, len(ivalue)):
					for x in range(0, len(ivalue[n])):
						if int(ivalue[n][x]) > int(value[i]):
							cdss[ikey][n][x]	= int(cdss[ikey][n][x]) + additions[key][i]
							exons[ikey][n][x]	= int(exons[ikey][n][x]) + additions[key][i]
gff	= open(options.gff, 'r')
outfile	= open(options.prefix+".gff", 'w')
for line in gff.readlines():
	fields		= line.split()
	if fields[2] == "gene":
		name	= fields[8].split(";")[0][3:]
		string	= "\t".join([chromosomes[name], "Corrected", "gene", str(genes[name][0]), str(genes[name][1]), str(sources[name]), str(strands[name]), str(phases[name]), "ID="+name]) + "\n"
		outfile.write(string)
		string	= "\t".join([chromosomes[name], "Corrected", "mRNA",  str(genes[name][0]), str(genes[name][1]), str(sources[name]), str(strands[name]), str(phases[name]), "ID=mrna."+name+";Parent="+name]) + "\n"
		outfile.write(string)
		for i in range(0, len(cdss[name])):
			string	= "\t".join([chromosomes[name], "Corrected", "CDS",  str(cdss[name][i][0]), str(cdss[name][i][1]), str(cdssources[name][i]), str(cdsstrands[name][i]), str(cdsphases[name][i]), "ID=cds."+name+";Parent="+name]) + "\n"
			outfile.write(string) 
			string	= "\t".join([chromosomes[name], "Corrected", "exon",  str(exons[name][i][0]), str(exons[name][i][1]), str(exonsources[name][i]), str(exonstrands[name][i]), str(exonphases[name][i]), "ID=exon."+name+";Parent="+name]) + "\n"
			outfile.write(string)
gff.close()
outfile.close()
print "Done"
