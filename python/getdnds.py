#!/usr/bin/env python

import argparse
import re
from subprocess import call
from Bio.Phylo.PAML import codeml
import os

parser	= argparse.ArgumentParser()

parser.add_argument(	'-a',
			dest='reference',
			metavar='REFERENCE',
			help='Reference genome.'	)


parser.add_argument(	'-b',
			dest='vcf',
			metavar='VCF',
			help='Vcf with SNPs.'	)

parser.add_argument(	'-c',
			dest='cdss',
			metavar='CDS',
			help='Gff file containing only sorted CDS sequences.'	)

parser.add_argument(	'-d',
			dest='gatk',
			metavar='GATK',
			help='Full path to GATK jar file.'	)

parser.add_argument(	'-e',
			dest='referencecds',
			metavar='REFERENCE CDS',
			help='Fasta file containing concatenated reference CDS sequences for genes of interest.'	)

parser.add_argument(	'-f',
			dest='translatorx',
			metavar='TRANSLATORX',
			help='Full path to translatorX script.'	)

parser.add_argument(	'-g',
			dest='codeml',
			metavar='CODEML CONTROL',
			help='codeml control file.'	)

parser.add_argument(	'-i',
			dest='output',
			metavar='PREFIX',
			default="out",
			help='Prefix for output files. Defaults to "out".'	)

options	= parser.parse_args()	

if not options.reference or not options.vcf or not options.cdss or not options.gatk or not options.referencecds or not options.translatorx or not options.codeml:
	parser.error("Please specify all input files.")

def getList(gff):
	with open(gff, 'r') as fh:
		cdsnames	= list()
		for line in fh.readlines():
			if not re.match("^#", line):
				fields	= line.split()
				name	= fields[8].split(";")[0][3:].split(".")[2]
				if name not in cdsnames:
					cdsnames.append(name)
	fh.close()
	return cdsnames

def dndsCalc(cdsnames, fastaa, fastab):
	results	= dict()
	for item in cdsnames:
		outfile	= open(item + ".fasta", "w")
		call(["awk", '{if($0~/>/){sw=0};if($0~/'+item+'/){sw=1};if(sw==1){print $0}}', fastaa], stdout=outfile)
		call(["awk", '{if($0~/>/){sw=0};if($0~/'+item+'/){sw=1};if(sw==1){print $0}}', fastab], stdout=outfile)
		outfile.close()
		call([options.translatorx, "-i", item + ".fasta", "-o", item])
		with open(options.codeml, 'r') as fh:
			outfile	= open(options.output + ".tmpcodeml", "w")
			for line in fh.readlines():
				if re.match("seqfile", line):
					fields	= line.split("=")
					line	= fields[0]+"="+item+".nt_ali.fasta" + "\n"
				if re.match("outfile", line):
					fields	= line.split("=")
					line	= fields[0]+"="+item+".ind.dnds"+"\n"
				outfile.write(line)
		outfile.close()
		call(["mv", options.output +".tmpcodeml", "codeml.ctl"])
		call(["touch", "treefile.txt"])
		call(["codeml"])
def cleanUp():
	for item in cdsnames:
		os.system("rm "+ item + "*")
	os.system("rm codeml.ctl")
	os.system("rm 2* 4* rst* rub")
	os.system("rm treefile.txt")

def reformatGff(gff):
	with open(gff, 'r') as fh:
		outfile	= open(output + ".reformattedGff.gff", 'w')
		for line in fh.readlines():
			if not re.match("^#", line):
				fields	= line.split()
				fields[3]	= int(fields[3]) - 1
				string		= "\t".join([fields[0],fields[1], fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],fields[8]]) + "\n"
				outfile.write(string)
	fh.close()
	outfile.close()

def gffToBed (gff, output):
	with open(gff, 'r') as fh:
		outfile	= open(output + ".reformattedGff.bed", 'w')
		for line in fh.readlines():
			if not re.match("^#", line):
				fields	= line.split()
				string	= '\t'.join([fields[0], str(int(fields[3]) - 1), fields[4], fields[5], fields[6], fields[8]]) + "\n"
				outfile.write(string)
	fh.close()
	outfile.close()
			
gffToBed(options.cdss, options.output)
	
call([	"java", "-jar", options.gatk,
	"-T", "FastaAlternateReferenceMaker",
	"-R", options.reference,
	"-o", options.output + ".alternate.fasta",
	"--variant", options.vcf,
	"-L", options.output + ".reformattedGff.bed"	])

call([	"joinCDS.py", "-a", options.cdss, 
	"-b", options.output + ".alternate.fasta", 
	"-c", options.output + ".mutated"	])

cdsnames	= getList(options.cdss)
dndsCalc(cdsnames, options.referencecds, options.output+".mutated.cds.fa")

os.system("cat *.ind.dnds > " + options.output + ".all.dnds")

cleanUp()	
