import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pakistan House Price Estimator")
st.title("Pakistan House Price Estimator")
st.write("A rough estimate of the asking price of a house for sale, based on about 93,000 Zameen.com listings.")


@st.cache_resource
def load_model():
    return joblib.load("models/house_price_model.joblib")


@st.cache_data
def load_data():
    return pd.read_csv("data/houses_clean.csv")


model = load_model()
df = load_data()

city = st.selectbox("City", sorted(df["city"].unique()))
locations = sorted(df.loc[df["city"] == city, "location"].unique())
location = st.selectbox("Location", locations)
area = st.number_input("Area (Marla)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=4)
baths = st.number_input("Baths", min_value=0, max_value=10, value=4)

if st.button("Estimate price"):
    row = pd.DataFrame([{
        "city": city,
        "location": location,
        "area_marla": area,
        "bedrooms": bedrooms,
        "baths": baths,
    }])
    price = model.predict(row)[0]
    st.success(f"Estimated asking price: {price / 10_000_000:.2f} crore (Rs {price:,.0f})")
    st.caption("Rough estimate only. It uses asking prices, not final sale prices, and ignores house condition and age.")