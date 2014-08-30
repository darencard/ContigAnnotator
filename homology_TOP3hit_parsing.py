id_dict = {}

for row in top3blast
	if row[0] not in id_dict.keys()
		id_dict[row[0]] = 1

## Do for one-way blast
## Assuming blast hits are ordered from best to worst e-value
for key in id_dict()
	list = []
	for row in top3blast
		if row[0] = key
			list.append entire.row
	for rows from 0 to len(list)
		if len(list) == 1
			first = row[0]
			print row[0] to first_hits.tsv
		elif len(list) == 2
			first = row[0]
			print row[0] to first_hits.tsv
			second = row[1]
			print row[1] to second_hits.tsv
		else
			first = row[0]
			print row[0] to first_hits.tsv
			second = row[1]
			print row[1] to second_hits.tsv
			third = row[2]
			print row[2] to third_hits.tsv

## Do for reciprocal blast
## Assuming blast hits are ordered from best to worst e-value
for key in id_dict()
	list = []
	for row in top3blast
		if row[0] = key
			list.append entire.row
	for rows from 0 to len(list)
		if len(list) == 1
			first = row[0]
			print row[0] to first_hits.tsv
		elif len(list) == 2
			first = row[0]
			print row[0] to first_hits.tsv
			second = row[1]
			print row[1] to second_hits.tsv
		else
			first = row[0]
			print row[0] to first_hits.tsv
			second = row[1]
			print row[1] to second_hits.tsv
			third = row[2]
			print row[2] to third_hits.tsv
			
## reciprocal hits analysis
one-way		reciprocal
first_hits	second_hits
second_hits	first_hits
first_hits	third_hits
third_hits	first_hits
second_hits	second_hits
second_hits	third_hits
third_hits	second_hits
third_hits	third_hits