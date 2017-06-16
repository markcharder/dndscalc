#!/usr/bin/env bash

GATK=/path/to/gatk.jar # Modify to the path to the gatk jar file.
REFERENCE=/path/to/reference.fa # Modify to get reference fasta.
VCFS=($(ls /path/to/all/vcfs/*)) # Modfiy to get a list of all vcfs to be considered.
INTERVALS=/path/to/intervals/file.bed # Modify to get intervals bed file.

# Had to run this first as gatk takes sequence from the next base up in a bed file:
# awk 'BEGIN{OFS="\t"}{print $1,$4-1,$5,".",".",$7}' /path/to/CDS.gff3 > /path/to/intervals/file.bed
# Note removed overlapping genes from gff3 file beforehand as it muddled up the output
# from gatk. The fastaAlternateReferenceMaker tool merges overlapping features.
# The variant files used in this analysis have been filtered. Only those that 'PASS' the thresholds
# of the hardfilter and recalibration have been kept.
for file in ${VCFS[@]}; do
	prefix=${file%.*}
	prefix=${prefix##*/}
	java -jar $GATK \
		-T FastaAlternateReferenceMaker \
		-R $REFERENCE \
		-o $prefix.alternate.fa \
		--variant $file \
		-L 
	awk '{if ($0 ~ />/){split($2,a,":"); print ">"a[1]}else{print $0}}' $prefix.alternate.fa > temp
	mv temp $prefix.alternate.fa
done
