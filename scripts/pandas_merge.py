#!/bin/env python3

import sys
import pandas as pd

df=pd.read_csv(sys.argv[1],index_col=0)
df2=pd.read_csv(sys.argv[2],index_col=0)
df3=pd.merge(df, df2, left_index=True, right_index=True)
df3.to_csv(sys.argv[3])
