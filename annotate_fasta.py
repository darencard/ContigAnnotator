#!/usr/local/env python

#print(__name__

from __future__ import print_function
import optparse
import json
from Bio import SeqIO

usage_line = """
annotate_fasta.py

Version 1.0 (28 August, 2014)
License: GNU GPLv2
To report bugs or errors, please contact Daren Card (dcard@uta.edu).
This script is provided as-is, with no support and no guarantee of proper or desirable functioning.

Script that annotates assembly contigs (fasta format) using a pre-made dictionary that is based \
upon reciprocal best blast and one-way blast results using an well-annotated genome (e.g., Ensembl), which \
indicates homology. The 'make_annotation_dictionary.py' script must be run first to build the annotation \
dictionary. Input is an assembly in fasta format and the output dictionary from the 'make_annotation_dictionary.py' \
script (in json format). Output is an annotated fasta assembly with transcript annotation IDs \
(e.g., Ensembl IDs) indicated in the contig headers. Also outputs the percentage of contigs that were annotated to \
STOUT.

python annotate_fasta.py -d <dictionary> -i <input_fasta> -o <output_fasta>"""

#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", action="store", type = "string", dest = "dictionary", help = "premade annotation dictionary")
parser.add_option("-i", action="store", type = "string", dest = "input", help = "input fasta sequence file")
parser.add_option("-o", action="store", type = "string", dest = "output", help = "output fasta sequence file")

options, args = parser.parse_args()

#################################################
###        Parse Annotation Dictionary	      ###
#################################################

## Establish decoding scheme to make all elements strings (read in as unicode)
def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

## Open the json annotation dictionary and load it into dictionary element with decoding	
if options.dictionary is None:		## If there is no annotation dictionary specified
	print("\n***Error: specify input annotation dictionary!***\n")
else:								## Annotation dictionary is specified!
	print("\n***Parsing in pre-created annotation dictionary from file***\n")
	with open(options.dictionary, "rb") as infile:
		annotation_dict = json.load(infile, object_hook=_decode_dict)
	#print(annotation_dict)
		
		
#################################################
###       		  Annotate Fasta        	  ###
#################################################

def annotate():
	if options.input is None:												## If there is no input specified
		print("\n***Error: specify input fasta file!***\n")
	if options.output is None:												## If there is no output specified
		print("\n***Error: specify output fasta file!***\n")
	else:																	## If both input and output are specified
		print("\n***Annotating assembly fasta headers***\n")
		output = open(options.output, "w")									## Create writeable output file using user-supplied name
		infile = open(options.input, "rU")
		total = 0															## Initialize total contigs counter
		annotated = 0														## Initialize annotated contigs counter
		assembly = SeqIO.parse(infile, "fasta")								## Open input and split by fasta
		for sequence in assembly:											## For each sequence
			total += 1
			print(total, end='\r')
			denovo = sequence.id
#			print(denovo)
			if denovo in annotation_dict.keys():							## If de novo assembly transcript name is in dictionary keys
				annotated += 1
				line = str(">"+annotation_dict[denovo]+"\n"+sequence.seq+"\n")		## Write fasta line with new ensembl id as header
				output.write(line)
			else:															## If no matching EnsemblID (i.e., no annotation)
				line = str(">"+"unannotated_"+sequence.id+"\n"+sequence.seq+"\n")	## Write fasta line with "unannotated_de novo id as header
				output.write(line)

		print("Total contigs:\t"+str(total))									##calculate basic statistics on annotation
		print("Total annotated:\t"+str(annotated))
		print("Percent annotated:\t"+str((float(annotated)/total)*100))
				
annotate()