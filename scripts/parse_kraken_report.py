#!/bin/env python3

import sys

taxa={}

total=0
with open(sys.argv[1],"r") as un:
    for x in un:
        line=x.split()
        if line[3]=="S1":
            taxon=' '.join(line[5:])
            taxa[taxon]=int(line[1])
            total+=int(line[1])

with open(sys.argv[2],"w") as parse:
    parse.write("Taxon,Relative Abundance,Read Counts\n")

    for k,v in taxa.items():
        rel=v/total
        abund=round(rel,4)
        if abund > 0:
            parse.write(f"{k},{abund},{v}\n")
