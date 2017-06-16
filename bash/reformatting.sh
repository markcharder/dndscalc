#!/usr/bin/env bash

# These scripts were used for reformatting the files for codeml analysis after using joinCDSs.py

for file in ./*joined*cds*fa; do awk '{if ($0 ~ />/){split(FILENAME,a,"."); split(a[2],b,"/"); print $0"|"b[2]}else{print $0}}' $file >> all_genes.fa; done

awk '{if ($0 ~ />/){header = $0; split($0,a,">"); split(a[2],b,":"); split(b[1],c,"_"); split($0,x,"|"); print ">"c[1]"|"x[2] >> c[1]".cds.fa"}else{print $0 >> c[1]".cds.fa"}}' all_genes.fa

# This was used for reformatting codeml output to get just the dN/dS ratios for each pairwise comparison.
for file in *.nt_ali.txt; do prefix=${file%.*}; awk 'BEGIN{OFS="\t"}{if($0~/ \(/){split($2,a,"|");split($5,b,"|"); split(a[2],c,")"); split(b[2],d,")"); r=c[1]; al=d[1]}; if ($0~/dN\/dS=/){print r,al, $8}}' $file > $prefix.dnds.txt; done

# This was used to add the reference sequences for each gene to all the fastas.
for file in {2..16}; do cd Chr_$file; awk -v file="$file" '{if(file < 10){if($0 ~ />/){split($0,a,">");header=a[2]}; if (header ~ "Sscle0"file){if ($0 ~ />/){print header"|1980" >> header".cds.fa"}else{print $0 >> header".cds.fa"}}}else{if($0 ~ />/){split($0,a,">");header=a[2]}; if (header ~ "Sscle"file){if ($0 ~ />/){print header"|1980" >> header".cds.fa"}else{print $0 >> header".cds.fa"}}}}' ../Ssclerotiorum_v2.cds.fasta; cd ..; done
