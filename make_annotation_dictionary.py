#!/usr/local/env python

#print(__name__

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
which actually annotate count (expression) tables and genome/transcriptome assembly contigs (fasta). \
Input is tabular output from a reciprocal best-hit and/or one-way blast between the genome/transcriptome of \
interest and a high-quality, annotated genome with target contig IDs as column 1 and reference contig \
IDs as column 2. Output is a json formatted version of the dictionary that may be named by the user.

python make_annotation_dictionary.py -r <RBH_output> -b <one-way_output> [-o <dictionary>]"""


#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("-r", action="store", type = "string", dest = "reciprocal", help = "reciprocal best-blast output")
parser.add_option("-b", action="store", type = "string", dest = "oneway", help = "one-way best-blast output")
parser.add_option("-o", action="store", type = "string", dest = "output", help = "output dictionary", default = "assembly_dictionary.json")

options, args = parser.parse_args()

## Establish dictionary
annotation_dict = {}

#################################################
###           	Read RBH output	   	          ###
#################################################
	
def rbh_in():
	if options.reciprocal is None:									## If no rbh output was specified
		print("\n***Error: specify reciprocal best-blast output!***\n")
	else:															## If necessary rbh output was specified
		total = 0
		print("\n***Parsing reciprocal best-blast output***\n")
		for foo in open(options.reciprocal).read().splitlines():	## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_rbh"										## blast match Ensembl ID
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value
		

#################################################
###         Read one-way blast output         ###
#################################################

def oneway_in():
	if options.oneway is None:										## If no oneway output was specified
		print("\n***Error: specify one-way best-blast output!***\n")
	else:															## If necessary rbh output was specified	
		total = 0
		print("\n\n***Parsing oneway best-blast output***\n")
		for foo in open(options.oneway).read().splitlines():		## Open file and split by lines
			total += 1
			print(total, end='\r')
			bar = foo.split()										## Split by tabs
			denovo = bar[0]											## de novo transcriptome ID
			ensembl = bar[1]+"_one"
			if denovo not in annotation_dict.keys():				## If de novo ID not already in keys
				annotation_dict[denovo] = ensembl					## Put de novo id as key and ensembl id as value


#################################################
###         	  Store dictionary            ###
#################################################

## Store the created dictionary with both rbh and oneway results into an output file for storage and input into annotation scripts		
def store_dict():
	with open(options.output, "wb") as outfile:						
		json.dump(annotation_dict, outfile)

				
rbh_in()
oneway_in()
store_dict()