import os
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, median_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import TargetEncoder

df = pd.read_csv("data/houses_clean.csv")

X = df[["city", "location", "area_marla", "bedrooms", "baths"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

baseline = [y_train.median()] * len(y_test)
print("Baseline average error:", f"{mean_absolute_error(y_test, baseline):,.0f}")
print("Baseline typical error:", f"{median_absolute_error(y_test, baseline):,.0f}")

prep = ColumnTransformer(
    [("places", TargetEncoder(target_type="continuous", random_state=42),
      ["city", "location"])],
    remainder="passthrough",
)

model = TransformedTargetRegressor(
    regressor=Pipeline([
        ("prep", prep),
        ("gbm", HistGradientBoostingRegressor(random_state=42)),
    ]),
    func=np.log1p,
    inverse_func=np.expm1,
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("Model average error:", f"{mean_absolute_error(y_test, predictions):,.0f}")
print("Model typical error:", f"{median_absolute_error(y_test, predictions):,.0f}")
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/house_price_model.joblib")

samples = pd.DataFrame([
    {"city": "Islamabad", "location": "F-7", "area_marla": 10, "bedrooms": 5, "baths": 5},
    {"city": "Islamabad", "location": "G-13", "area_marla": 10, "bedrooms": 5, "baths": 5},
])
for place, price in zip(["F-7", "G-13"], model.predict(samples)):
    print(f"10 Marla house in {place}: {price:,.0f} rupees")
    df[["city", "location"]].drop_duplicates().sort_values(["city", "location"]).to_csv(
    "models/locations.csv", index=False
)