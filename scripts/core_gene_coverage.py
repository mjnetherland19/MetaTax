import sys
import re
import json

path="/mnt/e/NCBI_Best_Prokaryote_Genomes/Arius_Shotgun_DB/ucg"

with open(f"{path}/{ucg}","r") as f:
    data = f.read()

d2 = json.loads(data)

with open(bedfile,"r") as bed:
    for x in bed:
        ref,start,end,query,mapq,strand=x.split("\t")

for key in d2["data"].keys():
    if len(d2["data"][key]) > 0:
        dna_seq=d2["data"][key][0]["dna"]

