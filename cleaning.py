import pandas as pd

from matplotlib import pyplot as plot
df = pd.read_csv("mushrooms.csv")
# df['id'] = [i + 1 for i in range(len(df))]


df.to_csv("mushrooms.csv")
df = pd.read_csv("mushrooms.csv")
print(df)
col = list(df.columns)
print(col)
# df1 = pd.read_csv("mushrooms.csv")
# print(df1)
# print(len(df))
# df["Place of Publication"] = df["Place of Publication"].apply(lambda x: "London" if "London" in x else x.replace('-', ' '))