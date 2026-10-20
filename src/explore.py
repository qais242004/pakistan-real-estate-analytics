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

print("area over 100 Marla:", (df["area_marla"] > 100).sum())
print("bedrooms over 10:", (df["bedrooms"] > 10).sum())
print("baths over 10:", (df["baths"] > 10).sum())
print("price over 20 crore:", (df["price"] > 200_000_000).sum())