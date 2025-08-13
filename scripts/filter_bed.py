#!/bin/env python3

import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],sep="\t",names=["Ref","Start","End","Query","Qual","Strand"])
qual=int(sys.argv[2])
out=sys.argv[3]

df=df.loc[df["Qual"]>qual]

df.to_csv(f"{out}/filtered_{qual}.bed",sep="\t",index=False,header=False)
