#!/usr/local/env python

#print __name__

import optparse
import os

usage_line = """
homology_blast.py

Version 1.0 (28 August, 2014)
License: GNU GPLv2
To report bugs or errors, please contact Daren Card (dcard@uta.edu).
This script is provided as-is, with no support and no guarantee of proper or desirable functioning.

Script that performs desired reciprocal blasting that is used as the basis for inferring homology between a \
reference and a target genome for the purposes of annotation. Script takes both reference and target contigs \
(fasta) and corresponding names and/or IDs, and will also run a user-defined blast tool (e.g., tblastx) and \
will only keep hits with an e-value below that specified by the user. A '--run' option is also available for \
circumstances where multiple blasts may be run, so as to not unnecessarily repeat blast database creation. \
In this circumstance, the user passes the numbers 1 (=blast database creation) or 2 (=reciprocal blast) for \
the '--run' option (e.g., '--run 12')

python homology_blast.py -r <reference_fasta> -t <target_fasta> --reference <reference_name> \
--target <target_name> -b <blast_type> -e <e-value> [-r <12>]"""


#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("-r", action = "store", type = "string", dest = "reference", help = "reference contigs (fasta)")
parser.add_option("-t", action = "store", type = "string", dest = "target", help = "target contigs (fasta)")
parser.add_option("-b", action = "store", type = "string", dest = "blast", help = "type of blast")
parser.add_option("-e", action = "store", type = "string", dest = "evalue", help = "e-value threshold")
parser.add_option("--reference", action = "store", type = "string", dest = "refgen", help = "reference name or ID")
parser.add_option("--target", action = "store", type = "string", dest = "targen", help = "target name or ID")
parser.add_option("--run", action = "store", type = "string", dest = "run", help = "processes to run (1-2)", default = "12")
parser.add_option("--threads", action = "store", type = "string", dest = "threads", help = "the number of threads blast will use", default = "2")

options, args = parser.parse_args()


#################################################
###            Make blast databases           ###
#################################################

## command: makeblastdb -dbtype nucl -parse_seqids -in <input.fasta>

def makedb():
	print "\n***Creating a blast database for "+options.refgen+"***"
	os.system("makeblastdb -dbtype nucl -parse_seqids -in "+options.reference)
	print "\n***Creating a blast database for "+options.targen+"***"
	os.system("makeblastdb -dbtype nucl -parse_seqids -in "+options.target)


#################################################
###           		Run blasts 		          ###
#################################################

## command: <blast_type> -max_target_seqs 1 -outfmt 11 -evalue <evalue> -db <reference/target.fasta> \
## -query <reference/target.fasta> -out <db-name_TO_qry-name.out.asn>
## all blast hits are outputted to blast archive (option 11) format so they can be converted to any format later ##

def blast():
	print "\n***Blasting "+options.targen+" query against "+options.refgen+" database***"
	os.system(options.blast+" -num_threads "+options.threads+" -outfmt 11 -max_target_seqs 5 -evalue "+options.evalue+" -db "+options.reference+ \
	" -query "+options.target+" -out db-"+options.refgen+"_TO_qry-"+options.targen+"_e"+options.evalue+".out.asn")
	print "\n***Blasting "+options.refgen+" query against "+options.targen+" database***\n"
	os.system(options.blast+" -num_threads "+options.threads+" -outfmt 11 -max_target_seqs 5 -evalue "+options.evalue+" -db "+options.target+ \
	" -query "+options.reference+" -out db-"+options.targen+"_TO_qry-"+options.refgen+"_e"+options.evalue+".out.asn")

#################################################
###           		Main function             ###
#################################################

def main():
## Check for missing user input
	if options.reference is None:
		print "\n***Error: specify reference fasta file!***\n"
	elif options.target is None:
		print "\n***Error: specify target fasta file!***\n"
	elif options.refgen is None:
		print "\n***Error: specify a name or ID for your reference genome!***\n"
	elif options.targen is None:
		print "\n***Error: specify a name or ID for your target genome!***\n"
	elif options.blast is None:
		print "\n***Error: specify the type of blast you would like to use!***\n"
	elif options.evalue is None:
		print "\n***Error: specify the threshold e-value a blast hit must be less than!***\n"
## When all input is present, run user-specified processes (12 by default)
	else:
		if "1" in options.run:
			makedb()
		if "2" in options.run:
			blast()
		
main()
