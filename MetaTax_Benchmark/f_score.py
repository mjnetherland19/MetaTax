#!/bin/env python3
import sys
import re

#truth
truth={}

with open(sys.argv[1],"r") as tru:
    for t in tru:
        line=t.strip().split(",")[0]
        truth[line]=0
TP=0
FP=0
FN=0
false=set()
with open(sys.argv[2],"r") as res:
    for r in res:
        
        line=" ".join(r.strip().split(",")[0].split("_"))
        
        if line in truth.keys():
            truth[line]+=1
            TP+=1
        else:
            false.add(line)
FP=len(false)

for v in truth.values():
    if v == 0:
        FN+=1

Pres=TP/(TP+FP)
Reca=TP/(TP+FN)
F1=2*Pres*Reca/(Pres+Reca)

print(f"Sample {sys.argv[1].split("/")[-1].split("_")[0]}")
print("True Positives")
print(truth)
print()
print("False Positives")
print(false)
print()

print(f"F1-score: {round(F1,2)}, False Positives: {FP}")
print("-----------------------------------------------")
