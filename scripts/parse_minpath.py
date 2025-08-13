import sys
import re

fil=sys.argv[1]
save=fil.split("/")[-1].split("_")[0]

with open(sys.argv[1],"r") as minpath, open(f"{save}_minpath_melt.csv","w") as melt:
    for m in minpath:
        line=m.strip().split()
        line=line[7:]
        confirm=line[0]
        total=line[2]
        found=line[4]
        name=line[6:]
        name=" ".join(name)
        name=re.sub(",",";",name)

        if confirm == '1':
            melt.write(f"{name},{round(int(found)/int(total),2)},{save}\n")

