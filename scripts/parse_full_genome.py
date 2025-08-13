import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],sep="\t",names=["Ref","Start","End","Query","Qual","Strand"])
#print(df.head())
lizt=list(df["Ref"].unique())
for l in lizt:
    print(l)

#df.to_csv("filtered.bed",sep="\t",index=False,header=False)
