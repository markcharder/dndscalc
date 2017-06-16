#!/usr/bin/env bash

for file in `ls *.nt_ali.fasta`; do
	prefix=${file%.*}
	echo "seqfile = $file
	outfile = $prefix.txt
	treefile = treefile.txt
	noisy = 9
	verbose = 1
	runmode = -2
	seqtype = 1
	CodonFreq = 0
	model = 0
	NSsites = 0
	icode = 0
	fix_kappa = 0
	fix_omega = 0
	omega = 0.5" > codeml.ctl
	yes | codeml
done

