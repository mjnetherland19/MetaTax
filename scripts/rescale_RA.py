#!/bin/env python3

import sys
import re
import pandas as pd

taxa={}
fil=sys.argv[1]
out=sys.argv[2]

co=0
with open(fil,"r") as first:
    for f in first:
        taxon,ra,count=f.strip().split(",")
        co+=int(count)
        taxa[taxon]=[int(count)]
        co+=1
for k,v in taxa.items():
    taxa[k].append(round(taxa[k][0]/co,4))

df=pd.DataFrame.from_dict(taxa, orient='index',columns=['Counts','RA'])
df=df.sort_values("Counts",ascending=False)

df.to_csv(f"{out}_rescaled_RA.csv")
