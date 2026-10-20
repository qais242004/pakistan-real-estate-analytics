import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

query = """
select city, location, area_marla, bedrooms, baths, price
from clean.property
where purpose = 'For Sale'
  and property_type = 'House'
  and price is not null
  and area_marla is not null
"""

df = pd.read_sql(query, engine)
print("Rows before cleaning:", len(df))

df = df[~(df["area_marla"] > 100)]
df = df[~(df["bedrooms"] > 10)]
df = df[~(df["baths"] > 10)]

df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].median())
df["baths"] = df["baths"].fillna(df["baths"].median())

print("Rows after cleaning:", len(df))
print(df.isna().sum())
os.makedirs("data", exist_ok=True)
df.to_csv("data/houses_clean.csv", index=False)