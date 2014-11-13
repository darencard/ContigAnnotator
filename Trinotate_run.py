#!/usr/local/env python

##print __name__

import optparse
import os

usage_line = """
Trinotate_run.py

Version 1.0 (13 November, 2014)
License: GNU GPLv2
To report bugs or errors, please contact Daren Card (dcard@uta.edu).
This script is provided as-is, with no support and no guarantee of proper or desirable functioning.

This script runs the Trinotate annotation pipeline, which is meant to annotate transcriptome assemblies generated \
by the Trinity assembler. This relies on having Trinotate installed in the user's path, as well as all dependent programs: \
1. Trinity (specifically the "transdecoder" directory, the "support_scripts" directory, and the "rnammer_support" directory) \
2. sqlite \
3. NCBI Blast \
4. HMMER \
5. signalP v4 \
6. tmhmm v2 \
7. RNAMMER \

Links to these programs and minor installation notes are found on the Trinotate website (trinotate.sourceforge.net) \
and expanded documentation is provided with each software package. User must specify the Trinity assembly, the annotation \
databases desired (SwissProt, Uniref90, and/or Pfam-A). The default (recommendation) is to use the SwissProt and Pfam-A \
databases, but the user may also elect to use the Uniref90 (which is large and will likely greatly expand the run time). \

This script will automatically download and prepare the correct annotation databases, but there is also the option to provide \
the directory containing these prepared databases if they have already been prepared in a previous annotation. User can also set \
the number of threads to be used. See trinotate.sourceforge.net for more information and for full instructions. \

python Trinotate_run.py --trinity <trinity.fasta> --swissprot --pfam [--uniref]						
"""

#################################################
###           Parse command options           ###
#################################################

usage = usage_line
                        
parser = optparse.OptionParser(usage=usage)
parser.add_option("--trinity", action = "store", type = "string", dest = "trinity", help = "the transcriptome assembly generated by Trinity")
parser.add_option("--swissprot", action = "store_true", dest = "swissprot", help = "annotate using the SwissProt database", default = True)
parser.add_option("--pfam", action = "store_true", dest = "pfam", help = "annotate using the Pfam-A database", default = True)
parser.add_option("--uniref", action = "store_true", dest = "uniref", help = "annotate using the UniRef90 database", default = False)
parser.add_option("--databases", action = "store", type = "string", dest = "databases", help = "directory where annotation databases can be found")
parser.add_option("--threads", action = "store", type = "string", dest = "threads", help = "number of threads to use", default = "2")
parser.add_option("--output", action = "store", type = "string", dest = "output", help = "root name of the output annotation database and report")

options, args = parser.parse_args()



#################################################
###            	   Full Program               ###
#################################################

def prepare_databases():
	while options.swissprot == True:
		os.system("wget http://sourceforge.net/projects/trinotate/files/TRINOTATE_RESOURCES/20140708/uniprot_sprot.fasta.gz -P ./databases/")
		os.system("gunzip ./databases/uniprot_sprot.fasta.gz")
		os.system("makeblastdb -in ./databases/uniprot_sprot.fasta -dbtype prot")
	while options.pfam == True:
		os.system("wget http://sourceforge.net/projects/trinotate/files/TRINOTATE_RESOURCES/20140708/Pfam-A.hmm.gz -P ./databases/")
		os.system("gunzip ./databases/Pfam-A.hmm.gz")
		os.system("hmmpress ./databases/Pfam-A.hmm")
	while options.uniref == True:
		os.system("wget http://sourceforge.net/projects/trinotate/files/TRINOTATE_RESOURCES/20140708/uniref90.fasta.gz -P ./databases/")
		os.system("gunzip ./databases/uniref90.fasta.gz")
		os.system("makeblastdb -in ./databases/uniref90.fasta -dbtype prot")
	else:
		print "\n***Error: specify one or more annotation databases to use!***\n"



#################################################
###     	   Prepare Trinity Output         ###
#################################################
		
def trinity_prepare():
	os.system("TransDecoder -t "+options.trinity+" --CPU "+options.threads)
	os.system("get_Trinity_gene_to_trans_map.pl "+options.trinity+" > "+options.trinity+".gene_trans_map")



#################################################
###         	  Blast to Databases          ###
#################################################

def run_blast(directory):
	if options.swissprot == True:
		os.system("blastx -query "+options.trinity+" -db "+directory+"/uniprot_sprot.fasta -num_threads "+options.threads+" -max_target_seqs 1 -outfmt 6 > "+options.trinity+".uniprot.blastx.outfmt6")
		os.system("blastp -query "+options.trinity+".transdecoder.pep -db "+directory+"/uniprot_sprot.fasta -num_threads "+options.threads+" -max_target_seqs 1 -outfmt 6 > "+options.trinity+".uniprot.blastp.outfmt6")
	if options.uniref == True:
		os.system("blastx -query "+options.trinity+" -db "+directory+"/uniref90.fasta -num_threads "+options.threads+" -max_target_seqs 1 -outfmt 6 > "+options.trinity+".uniref90.blastx.outfmt6")
		os.system("blastp -query "+options.trinity+".transdecoder.pep -db "+directory+"/uniref90.fasta -num_threads "+options.threads+" -max_target_seqs 1 -outfmt 6 > "+options.trinity+".uniref90.blastp.outfmt6")



#################################################
###            	    Run HMMER                 ###
#################################################
		
def run_hmmer(directory):
	if options.pfam == True:
		os.system("hmmscan --cpu "+options.threads+"--domtblout "+options.trinity+".TrinotatePFAM.out "+directory+"/Pfam-A.hmm "+options.trinity+".trnasdecoder.pep > pfam.log")



#################################################
###            	   Run SignalP                ###
#################################################
		
def run_signalp():
	os.system("signalp -f short -n "+options.trinity+".signalp.out "+options.trinity+".transdecoder.pep")



#################################################
###             	  Run tmhmm               ###
#################################################
	
def run_tmhmm():
	os.system("tmhmm --short < "+options.trinity+".transdecoder.pep > "+options.trinity+".tmhmm.out")



#################################################
###            	     Run rnammer              ###
#################################################
	
def run_rnammer():
	os.system("RnammerTranscriptome.pl --transcriptome "+options.trinity+" --path_to_rnammer rnammer")



#################################################
###   Create Annotation Database and Report   ###
#################################################
	
def load_sqlite():
	os.system("""wget "http://sourceforge.net/projects/trinotate/files/TRINOTATE_RESOURCES/20140708/Trinotate.20140708.swissTrEMBL.sqlite.gz/download" -O """+options.output+""".sqlite.gz""")
	os.system("gunzip "+options.output+".sqlite.gz")
	os.system("Trinotate "+options.output+".sqlite init --gene_trans_map "+options.trinity+".gene_trans_map --transcript_fasta "+options.trinity+" --transdecoder_pep "+options.trinity+".transdecoder.pep")
	if options.swissprot == True:
		os.system("Trinotate "+options.output+".sqlite LOAD_swissprot_blastp "+options.trinity+".uniprot.blastp.outfmt6")
		os.system("Trinotate "+options.output+".sqlite LOAD_swissprot_blastx "+options.trinity+".uniprot.blastx.outfmt6")
	if options.uniref == True:
		os.system("Trinotate "+options.output+".sqlite LOAD_trembl_blastp "+options.trinity+".uniref90.blastp.outfmt6")
		os.system("Trinotate "+options.output+".sqlite LOAD_trembl_blastx "+options.trinity+".uniref90.blastx.outfmt6")
	os.system("Trinotate "+options.output+".sqlite LOAD_pfam "+options.trinity+".TrinotatePFAM.out")
	os.system("Trinotate "+options.output+".sqlite LOAD_tmhmm "+options.trinity+".tmhmm.out")
	os.system("Trinotate "+options.output+".sqlite LOAD_signalp "+options.trinity+".signalp.out")
	os.system("Trinotate "+options.output+".sqlite LOAD_rnammer "+options.trinity+".rnammer.gff")
	os.system("Trinotate "+options.output+".sqlite report > "+options.trinity+".report.xls")



#################################################
###            	   Full Program               ###
#################################################

def main():
	if options.databases is None:											# If reference is already indexed, can skip lengthy indexing
		os.system("mkdir databases")										# make 'mapping' directory (may error if already present)
		prepare_databases()
		directory = "databases"
	else:
		directory = options.databases
	trinity_prepare()
	run_blast(directory)
	run_hmmer(directory)
	run_signalp()
	run_tmhmm()
	run_rnammer()
	load_sqlite()
	


#################################################
###              Run Full Program             ###
#################################################
		
main()
		