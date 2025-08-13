import pandas as pd
import sys

df=pd.read_csv(sys.argv[1])
print(df.head())
df=df.drop_duplicates(subset="Taxon")

df.to_csv("temp_taxonomy.csv",index=False)
