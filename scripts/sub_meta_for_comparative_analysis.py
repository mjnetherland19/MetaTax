import sys
import re
import pandas as pd
import os

counts=sys.argv[1]
meta=sys.argv[2]
comp_out=sys.argv[3]

taxa=pd.read_csv(counts,index_col=0).T
meta=pd.read_csv(meta,index_col=0).fillna("NA")

m_cols=list(meta.columns)

for m in m_cols:
    out=f"{comp_out}/{m}"
    os.makedirs(out)
    temp=meta[m]
    merge=pd.merge(taxa,temp,left_index=True, right_index=True)
    sub=merge.loc[merge[m]!="NA"]
    sub_m=sub[m]
    df=sub.drop(columns=m)
    df.T.to_csv(f"{out}/{m}_taxa.csv")
    sub_m.to_csv(f"{out}/{m}_meta.csv")
    scan=list(sub_m)
    with open(f"{out}/{m}_scan.txt","w") as sc:
        for s in scan:
            sc.write(f"{s}\n")
