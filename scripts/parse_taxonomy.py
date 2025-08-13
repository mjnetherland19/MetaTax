import sys
import re
A=[]
with open(sys.argv[1],"r") as tax:
    for t in tax:
        if re.search("subsp",t):
            A.append(t.split(",")[-2])

for a in A:
    print(a)
