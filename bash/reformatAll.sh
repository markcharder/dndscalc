#!/usr/bin/env bash

# This script was used for reformatting files so that they are compatible with the R igraph package.

export PATH=$PATH:/home/mark/Analyses/2017/06.17/comparative_dnds/scripts/python
for file in *.nt_ali.dnds.txt; do

	prefix=${file%.*}
	reformatFiles.py $file > $prefix.reformat.txt

done
