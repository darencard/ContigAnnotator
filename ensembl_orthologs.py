#!/usr/local/env python

import optparse

usage_line = """
A script to extract orthologous Ensembl IDs from a genome-of-interest using a list \
of Ensembl IDs already in hand. Input is a list of Ensembl IDs and a "database" file \
downloaded from Ensembl that has the query Ensembl IDs in one column and the target/subject \
Ensembl IDs in another column. The user can also specify which column contains the \
query and the target Ensembl IDs and an output file name (tab-delimited text file). \

python ensembl_orthologs.py --query <query_list> --database <ensembl_database> \
-q <query_column> -s <subject_column> --output <output.txt>
"""

usage = usage_line

parser = optparse.OptionParser(usage=usage)
parser.add_option("--query", action= "store", type= "string", dest="query", help="""The query list of Ensembl IDs to find orthologs for""")
parser.add_option("--database", action="store", type= "string", dest="database", help="""A tab-delimited file with query IDs and subject IDs obtained from BioMart""")
parser.add_option("-q", action = "store", type = "string", dest = "q", help = """Column number where query IDs are located in "database" file (1, 2, ..., N)""")
parser.add_option("-s", action = "store", type = "string", dest = "s", help = """Column number where subject IDs are located in "database" file (1, 2, ..., N)""")
parser.add_option("--output", action = "store", type = "string", dest = "output" , help = """Output file to write results""", default = "output.txt")
options, args = parser.parse_args()


if __name__ == '__main__':
	db_dict = {}
	for line in open(options.database, "r"):
		if not line.strip().startswith("#"):
			record = line.rstrip().split("\t")
			q = str(options.q)
			s = str(options.s)
			query = int(q)-1
			subject = int(s)-1
			if len(record) == 2:
				db_dict[record[query]] = record[subject]
			else:
				db_dict[record[query]] = "NA"
	out = open(options.output, "w")
	for line in open(options.query, "r"):
		if not line.strip().startswith("#"):
			record = line.rstrip()
			value = db_dict[record]
			outline = record+"\t"+value+"\n"
			out.write(outline)
	out.close()
			