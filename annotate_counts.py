#!/usr/local/env python

#print __name__

import optparse
import json

usage_line = """
annotate_counts.py

Version 1.0 (28 August, 2014)
License: GNU GPLv2
To report bugs or errors, please contact Daren Card (dcard@uta.edu).
This script is provided as-is, with no support and no guarantee of proper or desirable functioning.

Script that annotates expression (counts) using a pre-made dictionary that is based \
upon reciprocal best blast and one-way blast results using an well-annotated genome (e.g., Ensembl), which \
indicates homology. The 'make_annotation_dictionary.py' script must be run first to build the annotation \
dictionary. Input is a tab-delimited count table (with transcript ID as first column) and the output dictionary \
from the 'make_annotation_dictionary.py' script (in json format). Output is an annotated count table with  \
transcript annotation IDs (e.g., Ensembl IDs) as the first column followed by all other input columns. \
It is best to use the 'annotate_fasta.py' script to annotate the reference before reads are mapped and \
counts are inferred.

python annotate_counts.py -d <dictionary> -i <input_counts> -o <output_counts>"""


#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", action="store", type = "string", dest = "dictionary", help = "premade annotation dictionary")
parser.add_option("-i", action="store", type = "string", dest = "input", help = "input count table (transcript ID as first column)")
parser.add_option("-o", action="store", type = "string", dest = "output", help = "output count table")

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
	print "\n***Error: specify input annotation dictionary!***\n"
else:								## Annotation dictionary is specified!
	print "\n***Parsing in pre-created annotation dictionary from file***\n"
	with open(options.dictionary, "rb") as infile:
		annotation_dict = json.load(infile, object_hook=_decode_dict)
	#print annotation_dict
		
		
#################################################
###       		  Annotate Table        	  ###
#################################################

def annotate():
	if options.input is None:									## If there is no input specified
		print "\n***Error: specify input count table!***\n"
	if options.output is None:									## If there is no output specified
		print "\n***Error: specify output count table!***\n"
	else:														## If both input and output are specified
		print "\n***Annotating count table***\n"
		output = open(options.output, "w")		# Create writeable output file using user-supplied name
		for foo in open(options.input).read().splitlines():		## Open input and split by lines
			bar = foo.split()									## Tab-split elements
			denovo = bar[0]
			if denovo in annotation_dict.keys():				## If de novo assembly transcript name is in dictionary keys
				line = annotation_dict[denovo]+"\t"+foo+"\n"	## Write EnsemblID<tab>original line
				output.write(line)
			elif denovo == "*":									## Retain special last line
				line = "*\t"+foo+"\n"							## Write *<tab>original line
				output.write(line)
			else:												## If no matching EnsemblID (i.e., no annotation)
				line = "unannotated_"+bar[0]+"\t"+foo+"\n"		## Write unannotated_denovoID<tab>original line
				output.write(line)
				
annotate()