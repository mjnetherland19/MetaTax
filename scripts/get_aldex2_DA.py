import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],index_col=0)
df=df.loc[df["wi.ep"]<0.05]
df=df.apply(lambda x: round(x,3))
df=df.rename(columns={f"effect":"Effect Size",f"wi.ep":"P-value",f"wi.eBH":"P-value (FDR corrected)"})
df=df[["Effect Size","P-value","P-value (FDR corrected)"]]
df.to_csv(f"{sys.argv[2]}_aldex2_DA.csv")
