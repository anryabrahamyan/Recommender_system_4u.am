# Import necessary libraries
import pandas as pd
import numpy as np
import plotly.express as px

# reading the dataframes
df = pd.read_csv('data/data.csv')
df2 = pd.read_csv("data/sample.csv")
# comment the above 2 rows and uncomment the below 2 rows
# if you want to specifically run the metrics.py
# df = pd.read_csv('data.csv')
# df2 = pd.read_csv("sample.csv")

# defining the metrics for cards
df2["time spent on item"] = np.random.rand(len(df2)) * 100 + 5

average_time = round(df2.groupby("UserID")["time spent on item"].mean().mean(), 4)

df2["Add to Cart indicator"] = np.random.rand(len(df2))
df2["Add to Cart indicator"] = (df2["Add to Cart indicator"] <= 0.2).astype(int)

total_revenue = round(
    df2[df2["Converted"] == 1]["ItemID"].apply(lambda x: df.iloc[x]["price"]).dropna().str.replace(",", "").astype(
        int).sum(), 4)

revenue_per_click = round(
    df2["ItemID"].apply(lambda x: df.iloc[x]["price"]).dropna().str.replace(",", "").astype(int).median(), 4)

conversion_rate = round(df2["Converted"].mean(), 4)

add_to_cart_rate = round(df2["Add to Cart indicator"].mean(), 4)

df3 = pd.merge(df2, df2["ItemID"].apply(lambda x: df.iloc[x]["price"]).dropna().str.replace(",", "").astype(int),
               right_index=True, left_index=True)

revenue_per_minute = round(df3["ItemID_y"].sum() / df3["time spent on item"].sum(), 4)

# modifications for the figure 1
df["price"] = df["price"].str.replace(",", "").astype(int)
df_ = df.groupby('category')["price"].sum()
df_ = df_.reset_index()
df_ = df_.sort_values("price")
fig1 = px.bar(df_, x="price", y="category", title="Revenue by category")

# modifications for the figure 2
df0 = pd.merge(df, df2, left_on=df.index, right_on="ItemID", how="inner")
df0_ = df0[df0["Converted"] == 1].groupby("brand")["price"].mean()
df0_ = df0_.reset_index()
df0_.rename(columns={"index": "brand"})
df0_ = df0_.sort_values('price', ascending=False).head(10)[['brand', 'price']]
fig2 = px.line_polar(df0_, r="price", theta='brand', line_close=True, title="Conversion Rate by Brand")

# modifications for the figure 3
df2_ = df0.groupby("store")['ItemID'].count()
df2_ = df2_.reset_index()
df2_.rename(columns={"index": "store"})
df2_ = df2_.sort_values('ItemID', ascending=False).head(10)[['store', 'ItemID']]
fig3 = px.bar_polar(df2_, r="ItemID", theta="store",
                    color="ItemID",
                    color_discrete_sequence=px.colors.sequential.Plasma_r, title='Recommended Count per Store')
