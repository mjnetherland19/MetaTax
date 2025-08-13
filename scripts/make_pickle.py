#!/bin/env python3
import pickle
import sys
import pandas as pd
import glob
import random

def rgb_to_hex(temp):
    return '#{:02x}{:02x}{:02x}'.format(temp[0], temp[1], temp[2])

def get_color():
    temp=[]
    for j in range(0,3):
        temp.append(random.randint(0, 255))

    return rgb_to_hex(temp)

#Comparateive DIR name
path=sys.argv[1]
out=sys.argv[2]

df=pd.read_csv(f"taxonomic_dataframes/species_taxonomy.csv",index_col=0)
taxonomic_rank=["Phylum","Class","Order","Family","Genus","Species"]

df=df.drop(columns=["Kingdom","Subspecies"])

sp=df.set_index("Species")

cols=taxonomic_rank.copy()
cols.remove("Species")

taxonomy=sp[cols]

no_tax=sp.drop(columns=cols)

colors={}
for r in list(taxonomy.columns):
    taxa_list=set(list(taxonomy[r]))
    for s in taxa_list:
        colors[s]=get_color()
for s in list(taxonomy.index):
    colors[s]=get_color()

df2=pd.read_csv(f"metadata.csv",index_col=0)

meta_cols=list(df2.columns)
Comps={}
for m in meta_cols:
    Set=set(list(df2[m]))
    use=Set.copy()
    for s in Set:
        if type(s) != type("s"):
            use.remove(s)
    comp_lab=sorted(use)
    Comps[m]=comp_lab

df4=pd.read_csv(f"full_dataset_diversities/total_alpha_diversity.csv",index_col=0)

df5=pd.read_csv(f"full_dataset_diversities/total_beta_diversity.csv",index_col=0)

##### Get Comparative Results ######
d={}
globs=glob.glob(f"{path}/*")

for g in globs:
    comp=g.split("/")[-1]
    al=pd.read_csv(f"{g}/{comp}_alpha_diversity.csv",index_col=0)
    b=pd.read_csv(f"{g}/{comp}_beta_diversity.csv",index_col=0)
    p=pd.read_csv(f"{g}/permanova.csv",index_col=0, usecols=[0,1,2,3,4,5]).fillna("")
    a=pd.read_csv(f"{g}/{comp}_aldex2_DA.csv",index_col=0)
    l=pd.read_csv(f"{g}/{comp}_linda_DA.csv",index_col=0)
    
    d[comp]=[al,b,p,a,l]


dfs=[df,taxonomy,no_tax,df2,df4,df5,d,colors,Comps]

with open(f'{out}/data.pkl', 'wb') as f:
    pickle.dump(dfs, f)

