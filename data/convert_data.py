import pickle as pkl
import pandas as pd

"""
Uncomment the commented codes to change pkl to csv type,
in order to work with it 
"""
# with open("data.pkl", "rb") as f:
#     object = pkl.load(f)

# df = pd.DataFrame(object)
df = pd.read_csv('data.csv')
df = df.dropna(subset=['price'])
# if the following line gives an error:
# change the type of price in excel to number (it's faster)
df = df.astype({'price':'int'})
df.to_csv(r'data.csv')
