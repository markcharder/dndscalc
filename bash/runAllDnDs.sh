#!/usr/bin/env bash

GATK=/home/mark/local/src/jar/GenomeAnalysisTK.jar
VCFS=/home/mark/Analyses/2017/06.17/snp_testing/data/merged_variants_filtered_renamed.vcf
REFERENCE=/home/mark/Rdrive/CCDM_Prog_10_Share-HANE0J-SE00128/Sclerotinia/smallRNAs/first/genomes/Ssclerotiorum_v2_sorted.fasta
RESULTS=/home/mark/Rdrive/CCDM_Prog_10_Share-HANE0J-SE00128/Sclerotinia/pan_genome/outputs/Local_05-17/dnds/results/all/
GFFCDS=/home/mark/Analyses/2017/05.17/smPolymorphisms/dnds/scripts/bash/Ssclerotiorum_v2_gene_models_reformatted_sorted_renamed.cds.gff3
GFFALL=/home/mark/Analyses/2017/05.17/smPolymorphisms/dnds/scripts/bash/Ssclerotiorum_v2_gene_models_reformatted_sorted_renamed.gff3
CODEML=/home/mark/Analyses/2017/05.17/smPolymorphisms/dnds/data/codeml.ctl

export PATH=/home/mark/Analyses/2017/05.17/smPolymorphisms/dnds/scripts/perl:/home/mark/Analyses/2017/05.17/smPolymorphisms/dnds/scripts/python:$PATH

if [ ! -d "$RESULTS" ];
then
	mkdir $RESULTS
fi

if [ ! -f "$RESULTS/genes.cds.fasta" ];
then
	gff2fasta.pl $REFERENCE $GFFALL $RESULTS/genes
fi

cd $RESULTS
for file in ${VCFS[@]};
do
	prefix=$file
	prefix=${file%.*}
	prefix=${prefix##*/}
	yes "\n" | getdnds.py \
	-a $REFERENCE \
	-b $file \
	-c $GFFCDS \
	-d $GATK \
	-e /home/mark/Rdrive/CCDM_Prog_10_Share-HANE0J-SE00128/Sclerotinia/localBackup/Research/2016/02.16/data/Ssclerotiorum_v2.cds.fasta \
	-f /home/mark/Analyses/2017/05.17/smPolymorphisms/dnds/scripts/perl/translatorX.pl \
	-g $CODEML \
	-i $RESULTS/$prefix
done

cat $RESULTS/$prefix*dnds > $RESULTS/all.dnds

parseCodeml.pl $RESULTS/all.dnds > all.filtered.dnds	
