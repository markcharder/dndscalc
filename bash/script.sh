#!/usr/bin/env bash


#for file in {2..16}; do cd Chr_$file; awk -v file="$file" '{if(file < 10){if($0 ~ />/){split($0,a,">");header=a[2]}; if (header ~ "Sscle0"file){if ($0 ~ />/){print header"|1980" >> header".cds.fa"}else{print $0 >> header".cds.fa"}}}else{if($0 ~ />/){split($0,a,">");header=a[2]}; if (header ~ "Sscle"file){if ($0 ~ />/){print header"|1980" >> header".cds.fa"}else{print $0 >> header".cds.fa"}}}}' ../Ssclerotiorum_v2.cds.fasta; cd ..; done

for file in Chr_{2..16}/*.fa; do awk '{if ($0 ~ "|1980"){print ">"$0}else{print $0}}' $file > temp; mv temp $file; done
