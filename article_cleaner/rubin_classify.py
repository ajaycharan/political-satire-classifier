import csv
import argparse
import json
import os
import re

for category in ['news', 'satire']:
    if not os.path.isdir(category):
        if  os.path.exists(category):
            print "%s exists but is not a directory" %category
        else:
            os.mkdir(category)

with open("Rubin_etal_NAACL_CADD_2016_Satirical_Legitimate_News_DB_RELEASED_0426_2016.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader)
    for i, row in enumerate(csvReader):
        if row[0] == '0':
            folderName = 'news'
        else:
            folderName = 'satire'
        with open(os.path.join(folderName, "%i.txt" %i), "w") as f:
            f.write(row[2])
