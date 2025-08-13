import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],index_col=0)
cols=list(df.columns)
pre=cols[1].split(".")[0]

df=df.loc[df[f"{pre}.pvalue"]<0.05]
df=df.apply(lambda x: round(x,3))
df=df.rename(columns={f"{pre}.log2FoldChange":"log2FoldChange",f"{pre}.pvalue":"P-value",f"{pre}.padj":"P-value (FDR corrected)"})
df=df[["log2FoldChange","P-value","P-value (FDR corrected)"]]
df.to_csv(f"{sys.argv[2]}_linda_DA.csv")
