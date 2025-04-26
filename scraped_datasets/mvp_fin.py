import pandas as pd

# Load dataset
df = pd.read_csv("mvp_fin.csv", encoding="ISO-8859-1")

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

# Rename columns
df.rename(columns={
    "player_row_player_name": "player_name",
    "player_row_player_age": "age",
    "player_row_player_club": "club",
    "player_row_player_market_value": "market_value",
    "player_row_player_nation": "nation"
}, inplace=True)

# Drop rows with missing critical fields
df.dropna(subset=["player_name", "age", "club", "market_value", "nation"], inplace=True)

# Convert age to numeric
df["age"] = pd.to_numeric(df["age"], errors="coerce")

df["market_value_million_eur"] = df["market_value"].apply(convert_euro_value)

# Drop original 'market_value' column
df.drop(columns=["market_value"], inplace=True)

# Reset index (optional)
df.reset_index(drop=True, inplace=True)

# Save cleaned dataset
df.to_csv("mvp_fin_cleaned.csv", index=False)

print("✅ mvp_fin.csv cleaned and saved as mvp_fin_cleaned.csv")
