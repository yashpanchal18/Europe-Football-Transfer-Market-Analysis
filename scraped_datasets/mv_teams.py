import pandas as pd

# Load dataset
df = pd.read_csv("mv_teams.csv", encoding="ISO-8859-1")

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
    "club_row_name_club": "club_name",
    "club_row_name_league": "league",
    "club_row_name_squad": "squad_size",
    "club_row_name_avg_age": "avg_age",
    "club_row_name_MV": "total_market_value",
    "club_row_name_avg_p_mv": "avg_player_market_value",
    "club_row_name_share_mv": "share_of_market_value"
}, inplace=True)

# Drop rows with missing critical values (club or market value)
df.dropna(subset=["club_name", "total_market_value"], inplace=True)


df["total_market_value_million_eur"] = df["total_market_value"].apply(convert_euro_value)
df["avg_player_market_value_million_eur"] = df["avg_player_market_value"].apply(convert_euro_value)

# Convert share of market value (e.g., "85.7 %") to float
df["share_of_market_value"] = df["share_of_market_value"].str.replace("%", "").str.strip()
df["share_of_market_value"] = pd.to_numeric(df["share_of_market_value"], errors="coerce")

# Drop original currency columns if not needed
df.drop(columns=["total_market_value", "avg_player_market_value"], inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

# Save cleaned data
df.to_csv("mv_teams_cleaned.csv", index=False)

print("✅ mv_teams.csv cleaned and saved as mv_teams_cleaned.csv")
