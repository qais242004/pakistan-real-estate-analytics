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
print(df.shape)
print(df.head())
print(df.isna().sum())