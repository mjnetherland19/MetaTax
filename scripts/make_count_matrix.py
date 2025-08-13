import sys
import re
import pandas as pd
import glob

data={}
data2={}
pre=sys.argv[1]
c=0
globs=glob.glob(f"{pre}*/*RA.csv")
for g in globs:
    samp=g.split("/")[0]
    first=[samp]
    with open(g,"r") as df:
        for d in df:
            if re.search("Counts",d):
                continue
            taxon,count,ra=d.strip().split(",")
            Count=first+[taxon,count]
            RA=first+[taxon,ra]
            data[c]=Count
            data2[c]=RA
            c+=1

df=pd.DataFrame.from_dict(data, orient='index',columns=['column','index','value'])
df=df.pivot(index='index',columns='column',values='value').fillna(0)
df.to_csv('taxonomic_dataframes/species_counts.csv')

df=pd.DataFrame.from_dict(data2, orient='index',columns=['column','index','value'])
df=df.pivot(index='index',columns='column',values='value').fillna(0)
df.to_csv('taxonomic_dataframes/species_RA.csv')
