import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],index_col=0)
taxonomy=pd.read_csv(sys.argv[2],index_col=0)

merge=pd.merge(taxonomy,df,left_index=True,right_index=True)

merge.to_csv("species_taxonomy.csv")
