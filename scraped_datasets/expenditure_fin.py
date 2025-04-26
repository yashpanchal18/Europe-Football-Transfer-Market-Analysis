import pandas as pd

# Load the updated dataset
df = pd.read_csv("expenditure_fin.csv", encoding="ISO-8859-1")

import re

def convert_euro_value(value):
    """
    Converts Euro strings like '€1.2bn', '€200.00m' into float in millions.
    Handles dirty encodings and missing/null values.
    """
    if pd.isna(value) or not isinstance(value, str):
        return None

    # Remove problematic encodings, whitespace
    value = value.replace('â\x82¬', '').replace('€', '').replace(',', '').strip()

    try:
        if 'bn' in value:
            return float(value.replace('bn', '').strip()) * 1000
        elif 'm' in value:
            return float(value.replace('m', '').strip())
        else:
            return float(value)  # in case already cleaned
    except ValueError:
        return None


# Split 'club_comps' into 'league' and 'season'
df[['league', 'season']] = df['club_comps'].str.extract(r'^(.*?)\s+(\d{2}/\d{2})$')

# Rename columns
df.rename(columns={
    "club_name": "club_name",
    "club_expend": "total_expenditure",
    "club_arrivals": "arrivals_count",
    "club_income": "total_income",
    "club_depart": "departures_count",
    "club_balance": "net_balance"
}, inplace=True)

# Apply the conversion
df["total_expenditure_million_eur"] = df["total_expenditure"].apply(convert_euro_value)
df["total_income_million_eur"] = df["total_income"].apply(convert_euro_value)
df["net_balance_million_eur"] = df["net_balance"].apply(convert_euro_value)

# Convert arrival/departure counts
df["arrivals_count"] = pd.to_numeric(df["arrivals_count"], errors='coerce')
df["departures_count"] = pd.to_numeric(df["departures_count"], errors='coerce')

# Drop old euro columns and 'club_comps'
df.drop(columns=["club_comps", "total_expenditure", "total_income", "net_balance"], inplace=True)

# Reorder columns for clarity
df = df[[
    "club_name", "league", "season",
    "arrivals_count", "departures_count",
    "total_expenditure_million_eur",
    "total_income_million_eur",
    "net_balance_million_eur"
]]

# Save cleaned data
df.to_csv("expenditure_fin_cleaned.csv", index=False)

print("✅ Cleaned dataset saved as expenditure_fin_cleaned.csv")
