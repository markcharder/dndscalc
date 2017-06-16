#!/usr/bin/env perl

use strict;
use warnings;

my $input	= $ARGV[0];

my $usage=<<USAGE;


	parseCodeml.pl
	**************

	parseCodeml.pl <codeml output>

	-	Prints dN/dS ratio to file for each first gene in pairwise alignment in codeml stdout.

USAGE

open my $FH, "<", $input or die ("\n\nPlease specify input file - output from codeml.\n\n$usage");

my %ids;
my $id;
while (my $line = <$FH>){
	if ($line =~ /^#1/){
		chomp $line;
		my @fields	= split /\s+/, $line;
		$id		= $fields[1];
	}
	elsif ($line =~ /dN\/dS=/){
		chomp $line;
		my @fields	= split /\s+/, $line;
		$ids{$id}	= $fields[7];
	}
	else{
		next;
	}
}

close $FH;

foreach my $key (keys %ids){
	print "$ARGV[0]\t$key\t$ids{$key}\n";
}

