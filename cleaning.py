import pandas as pd
from matplotlib import pyplot as plot
df = pd.read_csv("mushrooms.csv")
# df['id'] = [i + 1 for i in range(len(df))]
col = list(df.columns)
print(col)
# df.to_csv("mushrooms.csv", names=['Unnamed: 0','class','cap-shape','cap-surface','cap-color','bruises','odor','gill-attachment','gill-spacing','gill-size',gill-color,stalk-shape,stalk-root,stalk-surface-above-ring,stalk-surface-below-ring,stalk-color-above-ring,stalk-color-below-ring,veil-type,veil-color,ring-number,ring-type,spore-print-color,population,habitat,id])
# df1 = pd.read_csv("mushrooms.csv")
# print(df1)
# print(len(df))
# df["Place of Publication"] = df["Place of Publication"].apply(lambda x: "London" if "London" in x else x.replace('-', ' '))