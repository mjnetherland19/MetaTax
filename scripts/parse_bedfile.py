#!/bin/env python3
import sys
import re
import ast

def get_taxon(k):

    if re.search("jgi",k):
        return "_".join(k.split("_")[:1])
    else:
        return "_".join(k.split("_")[:2])

bedfile=sys.argv[1]
diction=sys.argv[2]
contents=sys.argv[3]
coverage=float(sys.argv[4])

with open(diction) as f: 
    data = f.read()

dic = ast.literal_eval(data)
dic1={}
dic2={}
for k,v in dic.items():
    dic2[v]=k
    dic1[k]=v

d2={}
with open(bedfile,"r") as bed:
    for x in bed:
        ref,start,end,query,mapq,strand=x.split("\t")
        base_ref=get_taxon(ref)
        
        # Make dictionary of {Taxon : [core genes found]}
        # to be used to calculate proportion of core genes found
        gene=ref.split("_")[-1]
        taxon=dic2[base_ref]
        if taxon not in d2.keys():
            d2[taxon]=[gene]
        else:
            if gene in d2[taxon]:
                continue
            else:
                d2[taxon].append(gene)
       

#Make {Domain:Species} dictionary
Contents={}
with open(contents,"r") as contents:
    for x in contents:
        line=x.split(",")
        Contents[line[0]]=line[1]
        #Contents[line[1]]=",".join(line[2:])

#Use {Domain:Species} dictionary to get proportion of core genes found
groups_written=[]
for k,v in d2.items():
    try:
        taxonomy=Contents[k]
        if re.search("Bacteria", taxonomy):
            cov=round(len(v)/81,2)
        elif re.search("Archaea", taxonomy):
            cov=round(len(v)/120,2)
        if re.search("Fungi", taxonomy):
            cov=round(len(v)/61,2)
        if cov >= coverage:
            if re.search("group",taxonomy):
                line=taxonomy.split(",")
                group=line[6]
                if group in groups_written:
                    continue
                else:
                    print(group)
                    groups_written.append(group)
            else:
                print(f"{k},{dic1[k]}")
    except:
        continue
