#!/usr/local/env python

#print__name__

from __future__ import print_function
import optparse
import json

usage_line = """
make_annotation_dictionary.py

Version 1.0 (28 August, 2014)
License: GNU GPLv2
To report bugs or errors, please contact Daren Card (dcard@uta.edu).
This script is provided as-is, with no support and no guarantee of proper or desirable functioning.

Script that takes formatted blast output from a reciprocal best-hit (RBH) or high-stringency one-way best-blast, \
which are meant to confidently infer homology, and creates an annotation dictionary. This annotation \
dictionary is simply a python dictionary that is outputted in json format for easy incorporation into \
other scripts, so that time-consuming dictionary creation doesn't have to be rerun multiple times. \
This script is meant to be run before the 'annotate_counts.py' and 'annotate_fasta.py' scripts, \
which actually annotate count (expression) tables and genome/transcriptome assembly contigs (fasta), respectively. \
Input is tabular output from a reciprocal best-hit and/or one-way blast between the genome/transcriptome of \
interest and a high-quality, annotated genome with target contig IDs as column 1 and reference contig \
IDs as column 2. Multiple input blast files can be designated - up to 3 reciprocal best-hit and 3 one-way
best-hit (script is annotated to allow addition of more) - and the user must specify the order in which they \
should be considered (i.e., rank the confidence of homology between blast inputs). Output is a json formatted \
version of the dictionary that may be named by the user. Errors will be written to STDOUT if user input is missing!

python make_annotation_dictionary.py --confidence rN,bN [--rN <RBH_output> --bN <one-way_output> --out <dictionary>]"""


#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("--r1", action = "store", type = "string", dest = "reciprocal1", help = "reciprocal best-blast output")
parser.add_option("--b1", action = "store", type = "string", dest = "oneway1", help = "one-way best-blast output")
parser.add_option("--r2", action = "store", type = "string", dest = "reciprocal2", help = "reciprocal best-blast output")
parser.add_option("--b2", action = "store", type = "string", dest = "oneway2", help = "one-way best-blast output")
parser.add_option("--r3", action = "store", type = "string", dest = "reciprocal3", help = "reciprocal best-blast output")
parser.add_option("--b3", action = "store", type = "string", dest = "oneway3", help = "one-way best-blast output")
## Note: To allow for more reciprocal/one-way blast input, copy the above definition(s) and adjust accordingly (e.g., --b3 -> --bN) ##
parser.add_option("--out", action = "store", type = "string", dest = "output", help = "output dictionary", default = "assembly_dictionary.json")
parser.add_option("--confidence", action = "store", type = "string", dest = "conf", help = "rank homology confidence of each blast input")

options, args = parser.parse_args()

## Establish dictionary
annotation_dict = {}

#################################################
###           	Read RBH output	   	          ###
#################################################
	
def r1_in():
	if options.reciprocal1 is None:									## If no rbh output was specified
		print("\n\n***Error: specify reciprocal best-blast output!***\n***Error: outputted assembly dictionary is incomplete!***")
	else:															## If necessary rbh output was specified
		total = 0
		print("\n\n***Parsing reciprocal best-blast output***\n")
		for foo in open(options.reciprocal1).read().splitlines():	## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_rbh1_"+bar[2]							## blast match Ensembl ID
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value

def r2_in():
	if options.reciprocal2 is None:									## If no rbh output was specified
		print("\n\n***Error: specify reciprocal best-blast output!***\n***Error: outputted assembly dictionary is incomplete!***")
	else:															## If necessary rbh output was specified
		total = 0
		print("\n\n***Parsing reciprocal best-blast output***\n")
		for foo in open(options.reciprocal2).read().splitlines():	## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_rbh2_"+bar[2]							## blast match Ensembl ID
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value
				
def r3_in():
	if options.reciprocal3 is None:									## If no rbh output was specified
		print("\n\n***Error: specify reciprocal best-blast output!***\n***Error: outputted assembly dictionary is incomplete!***")
	else:															## If necessary rbh output was specified
		total = 0
		print("\n\n***Parsing reciprocal best-blast output***\n")
		for foo in open(options.reciprocal3).read().splitlines():	## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_rbh3_"+bar[2]							## blast match Ensembl ID
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value
		
## Note: To allow for more reciprocal blast input, copy the above definition and adjust it accordingly (e.g., r3_in -> rN_in) ##

#################################################
###         Read one-way blast output         ###
#################################################

def b1_in():
	if options.oneway1 is None:										## If no oneway output was specified
		print("\n\n***Error: specify one-way best-blast output!***\n***Error: outputted assembly dictionary is incomplete!***")
	else:															## If necessary rbh output was specified	
		total = 0
		print("\n\n***Parsing oneway best-blast output***\n")
		for foo in open(options.oneway1).read().splitlines():		## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_one1_"+bar[2]
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value
				
def b2_in():
	if options.oneway2 is None:										## If no oneway output was specified
		print("\n\n***Error: specify one-way best-blast output!***\n***Error: outputted assembly dictionary is incomplete!***")
	else:															## If necessary rbh output was specified	
		total = 0
		print("\n\n***Parsing oneway best-blast output***\n")
		for foo in open(options.oneway2).read().splitlines():		## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_one2_"+bar[2]
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value
				
def b3_in():
	if options.oneway3 is None:										## If no oneway output was specified
		print("\n\n***Error: specify one-way best-blast output!***\n***Error: outputted assembly dictionary is incomplete!***")
	else:															## If necessary rbh output was specified	
		total = 0
		print("\n\n***Parsing oneway best-blast output***\n")
		for foo in open(options.oneway3).read().splitlines():		## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_one3_"+bar[2]
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value

## Note: To allow for more one-way blast input, copy the above definition and adjust it accordingly (e.g., r3_in -> rN_in) ##

#################################################
###         	  Store dictionary            ###
#################################################

## Store the created dictionary with both rbh and oneway results into an output file for storage and input into annotation scripts		
def store_dict():
	with open(options.output, "wb") as outfile:						
		json.dump(annotation_dict, outfile)

def main():
	if options.conf is None:
		print("\n***Error: specify the homology confidence ranking for all of your blast input files!***\n")
	else:
		order = options.conf.split(",")
		for x in range(0, len(order)):
			line = str(order[x])+"_in()"
			eval(line)
		store_dict()

main()
