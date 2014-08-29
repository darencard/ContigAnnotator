#!/usr/local/env python

#print __name__

import optparse
import os

usage_line = """
homology_BESThit_parsing.py

Version 1.0 (28 August, 2014)
License: GNU GPLv2
To report bugs or errors, please contact Daren Card (dcard@uta.edu).
This script is provided as-is, with no support and no guarantee of proper or desirable functioning.

Script that checks for reciprocal best-blast hits that are characteristic of homologous loci. Also outputs \
one-way best blast hits (target blasted against reference), which can also be confidently called homologous \
loci when the e-value in the 'homology_blasting.py' script is conservative enough. Inputs are the two \
blast archives outputted by the 'homology_blasting.py' script and desired names for the two output files \
(reciprocal best hit and one-way best hit). Note that the '-o' flag must be referencing the target to \
reference blast archive (reference = subject, target = query) in order for the one-way results to be \
correct. Outputs are tables with target ID in column 1 and reference ID in column 2. These results can \
be fed into the 'make_annotation_dictionary.py' script and subsequently used for annotating both \
contigs (fasta) and count tables.

python homology_hit_parsing.py -o <oneway_blast_results> -r <reciprocal_blast_results> --oneway <oneway_output> \
--reciprocal <reciprocal_best_blast_output>"""


#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("-o", action = "store", type = "string", dest = "oneway", help = "one-way blast results (target to reference)")
parser.add_option("-r", action = "store", type = "string", dest = "reciprocal", help = "reciprocal blast results")
parser.add_option("--oneway", action = "store", type = "string", dest = "oneout", help = "one-way blast output")
parser.add_option("--reciprocal", action = "store", type = "string", dest = "recout", help = "reciprocal blast output")

options, args = parser.parse_args()


#################################################
###            Convert blast archive          ###
#################################################

## convert each blast archive to a standard tab-delimited subject ID/query ID output for parsing
## command: blast_formatter -outfmt "6 sseqid qseqid" -archive <blast_archive> -out <output.tsv>

def convert():
	print "\n***Converting one-way target to reference blast archive***\n"
	os.system("""blast_formatter -max_target_seq 1 -outfmt "6 sseqid qseqid evalue" -archive """+options.oneway+""" -out one-way_best_hits.tsv""") 
	print "\n***Converting reciprocal reference to target blast archive***\n"
	os.system("""blast_formatter -max_target_seq 1 -outfmt "6 sseqid qseqid evalue" -archive """+options.reciprocal+""" -out reciprocal_best_hits.tsv""") 


#################################################
###             Parse one-way hits 		      ###
#################################################

## create dictionary with column 1 as key and column 2 as value for one-way blast results
oneway_dict = {}
def oneway():
	print "\n***Parsing one-way target to reference blast results***\n"
	for foo in open("one-way_best_hits.tsv").read().splitlines():
		bar = foo.split()
		subjectID = bar[0]
		queryID = bar[0]
		if subjectID not in oneway_dict.keys():
			oneway_dict[subjectID] = queryID
			

#################################################
###            Parse reciprocal hits 	      ###
#################################################

## create dictionary with column 1 as key and column 2 as value for reciprocal blast results
reciprocal_dict = {}
def reciprocal():
	print "\n***Parsing reciprocal reference to target blast results***\n"
	for foo in open("reciprocal_best_hits.tsv").read().splitlines():
		bar = foo.split()
		subjectID = bar[0]
		queryID = bar[0]
		if subjectID not in reciprocal_dict.keys():
			reciprocal_dict[subjectID] = queryID
			
			
#################################################
###       Check for reciprocal best hits      ###
#################################################

## check to see whether one-way best blast hit is reciprocally the best blast hit
rbh = {}
def rbh_analysis():
	print "\n***Performing reciprocal best blast analysis***\n"
	for key1 in oneway_dict.keys():
		value1 = oneway_dict[key1]
		if value1 in reciprocal_dict.keys():
			if key1 == reciprocal_dict[value1]:
				rbh[value1] = key1

## output file with target ID (fasta header) as column 1 and reference ID (fasta header) as column 2		
	outfile = open(options.recout, "w")
	for key in rbh.keys():
		line = key + '\t' + rbh[key] + '\n'
		outfile.write(line)
	outfile.close()
## also copy working one-way best blast (target blasted against reference) to desired output file name
	os.system("cp reciprocal_best_hits.tsv "+options.oneout)


#################################################
###           		Main function             ###
#################################################

def main():
## Check for missing user input
	if options.oneway is None:
		print "\n***Error: specify the one-way (target to reference) blast archive!***\n"
	elif options.reciprocal is None:
		print "\n***Error: specify the reciprocal (reference to target) blast archive!***\n"
	elif options.oneout is None:
		print "\n***Error: specify a file name for the one-way best-blast results!***\n"
	elif options.recout is None:
		print "\n***Error: specify a file name for the reciprocal best-blast results!***\n"
## When all input is present
	else:
		convert()
		oneway()
		reciprocal()
		rbh_analysis()
		
main()