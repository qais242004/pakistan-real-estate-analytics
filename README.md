# Pakistan Real Estate Analytics

End-to-end analysis of about 190,000 property listings from Zameen.com, using PostgreSQL (Supabase), SQL, Power BI and Python (scikit-learn).

## What this project does

1. Loads raw listings into a `raw` schema (never modified).
2. Cleans the data in a separate view, `clean.property`.
3. Answers business questions with SQL.
4. Shows the results in a Power BI dashboard.
5. Trains a model that estimates the asking price of a house.

## Data cleaning decisions

| Problem found | What I did | Why |
|---|---|---|
| 24,471 rows had 0 bedrooms and 0 baths | Set to NULL | Missing data saved as 0 would distort averages |
| 0 bedrooms in Flat and Room | Kept | Studio flats and single rooms are real |
| Area stored as text ("10 Marla", "1.1 Kanal") | Converted to numeric Marla (1 Kanal = 20 Marla) | Needed for price per Marla |
| 297 areas below 1 or above 2000 Marla | Set to NULL | Typos and bad entries |
| 127 prices too low (sale below 5 lakh, rent below 1000) | Set to NULL | Not realistic listings |

No rows were deleted in SQL. Bad values became NULL so other columns stay usable.

## Findings so far

- **Mixing property types gives a wrong picture.** Karachi looks third most expensive per Marla when all types are mixed, but it is the most expensive for houses only (about 27.9 lakh per Marla). The reason: 45.6% of Karachi listings are flats, compared with 4% in Lahore.
- **Islamabad's most expensive area is F-7** (about 48 lakh per Marla for houses), roughly double the city median. Five of the top 10 areas are in the F sector.
- **Estimated rental yield for houses** is highest in Karachi (4.57% per year) and lowest in Rawalpindi (3.84%). These use asking prices and ignore maintenance, tax and vacancy, so treat them as estimates.

All figures are medians, not averages, so a few extreme listings do not distort the result.

## Dashboard preview

![Power BI dashboard](images/dashboard.png)

## Price prediction model

A gradient boosting model (`HistGradientBoostingRegressor`) estimates the asking price of a house for sale from its city, location, area in Marla, bedrooms and baths.

**Data preparation**
- Started from 93,722 houses for sale and removed 479 rows that look like typos (area above 100 Marla, or more than 10 bedrooms or baths).
- Filled missing bedrooms and baths with the median.
- Kept very expensive houses, because many of them are real.

**Evaluation**
- 80% of the houses were used for training (74,594) and 20% for testing (18,649). The test houses were never seen during training.
- The model was compared with a simple baseline that gives every house the same median price.

| Error on unseen houses | Baseline | Model |
|---|---|---|
| Typical error (median) | 85 lakh | 20.9 lakh |
| Average error (mean) | 1.92 crore | 58.5 lakh |

The typical error is about four times smaller than the baseline. The average error is still large because very expensive houses are hard to predict.

**Example:** for the same 10 Marla house with 5 bedrooms and 5 baths, the model estimates about 4.6 crore in F-7 and about 2.9 crore in G-13 (Islamabad).

**Limitations**
- Prices are asking prices, not final sale prices.
- The model uses only five inputs, so it ignores things like house condition, age and exact street.
- It should be treated as a rough estimate.

## How to run

1. Install the libraries: `pip install pandas scikit-learn sqlalchemy psycopg2-binary python-dotenv matplotlib`
2. Create a `.env` file with your database address: `DATABASE_URL=...` (this file is never uploaded).
3. Run `python src/prepare_data.py` to clean the data and save it to `data/houses_clean.csv`.
4. Run `python src/train_model.py` to train and test the model.
5. Run `streamlit run src/app.py` to open the app.
## Streamlit app

A small web app lets you enter a city, location, area, bedrooms and baths and see the model's estimate of the asking price.

Run it with `streamlit run src/app.py` after training the model.

## Repository structure

- `sql/01_clean_property_view.sql`: cleaning view
- `sql/02_rental_yield.sql`: rental yield by city
- `src/prepare_data.py`: loads houses from the database, removes outliers, saves a clean CSV
- `src/train_model.py`: trains and tests the price model
- `src/load_data.py`, `src/explore.py`, `src/test_connection.py`: helper scripts
- `images/dashboard.png`: dashboard screenshot
- `src/app.py`: Streamlit app for trying the model
- `requirements.txt`: Python libraries needed to run the project
## Next steps

- Streamlit app to try the model with your own house details
- Track model results with MLflow