import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- Download ---
df = yf.download("PKR=X", start="2010-01-01", end="2025-01-01", interval="1d", group_by=False)
# Flatten by joining the levels with an underscore or something similar
df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col
              for col in df.columns]

df.dropna(inplace=True)   # remove rows with NaN
# If your flattened columns look like "PKR=X_Open", "PKR=X_High", etc.,
# remove the "PKR=X_" prefix:
df.columns = [col.replace("PKR=X_", "") for col in df.columns]

# Now columns should be "Open", "High", "Low", "Close", "Volume", etc.

print(df.head())
df = df[df["Close"] < 400]
df = df[df["Close"] > 60]

# Make sure the DataFrame's index is labeled
df.index.name = "Date"

# --- Save ---
csv_filename = "usd_to_pkr_historical_data.csv"
df.to_csv(csv_filename)  # Only 1 header row: "Date,Open,High..."

# --- Read back ---
df_from_csv = pd.read_csv(
    csv_filename,
    parse_dates=["Date"],
    index_col="Date"
)
print(df_from_csv.head())  # check

# Should now have a DatetimeIndex -> day_name() works
df_from_csv["DayOfWeek"] = df_from_csv.index.day_name()
df_from_csv["Pct_Change"] = df_from_csv["Close"].pct_change() * 100

avg_changes = df_from_csv.groupby("DayOfWeek")["Pct_Change"].mean()
print(avg_changes)
