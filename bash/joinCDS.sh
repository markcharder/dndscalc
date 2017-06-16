#!/usr/bin/env bash

# This should be run after running runGatk.sh.
# After running runGatk.sh, there will be results in the current directory suffixed with '.alternate.fa'. These are the
# alternate fasta sequences produced by GATK based on the coordinates provided in the reformatted bed file.
# For the python script to work, the supplied GFF must be sorted by chromosome then start position. 
# e.g. sort -V -k1,1 -k4,4 all_genes.cds.gff3 > temp; mv temp all_genes.cds.gff3

FASTAS=($(ls *alternate.fa)) # Modify if names have been changed.
GFF=/path/to/gff/with/CDS.gff3 # Modify to get the CDS intervals gff3 file.

for file in ${FASTAS[@]}; do
	prefix=${file%.*}
	prefix=${prefix##*/}
	../python/joinCDS.py \
		-a $GFF \
		-b $file \
		-c $prefix.joined > $prefix.txt
done
