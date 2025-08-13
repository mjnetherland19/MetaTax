import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],index_col=0)
df=df.apply(lambda x: x*100)
df.to_csv("species_percent.csv")
