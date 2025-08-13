#!/bin/env python3

#Change this script to use the prelim_map or seq2id in database

import sys
import json
import re
import ast

#List of species names
res=sys.argv[1]

#fasta_key.csv
path=sys.argv[2]

#pwd
pwd=sys.argv[3]
#pwd="/".join(path.split("/")[:-1])

with open(res,"r") as taxa:
    Taxa=[x.strip() for x in taxa]

key={}
with open(f"{path}/fasta_key.csv","r") as f, open(f"{pwd}/temp_multifasta","w") as temp:
    for x in f:
        taxon,acc,target=x.strip().split(",")
        if taxon in Taxa:
            with open(f"{path}/fasta/{target}.fasta","r") as tar:
                for t in tar:
                    #Format fasta header
                    if re.search(">",t):
                        gene_name=t.split("|")[0]
                        temp.write(f">{acc}_{gene_name[1:]}\n")
                    else:
                        temp.write(t)
