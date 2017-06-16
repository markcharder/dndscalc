#!/usr/bin/env bash

export PATH=$PATH:/home/mark/Analyses/2017/06.17/comparative_dnds/scripts/perl/

for file in  *.cds.fa; do
	prefix=${file%.*}
	translatorX.pl -i $file -o $prefix
done
