import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- 1) Download AED -> PKR historical data ---
df = yf.download(
    "AEDPKR=X",
    start="2010-01-01",
    end="2025-01-01",
    interval="1d"
)

# --- 2) Quick Peek ---
print(df.head())
print(df.tail())

# --- 3) Basic Data Cleanup ---
df.dropna(inplace=True)

# --- 4) Check & Drop Outliers ---
#   If you see an unrealistic spike, adjust these thresholds as needed for AED/PKR.
outliers = df[df["Close"] > 400]
print("Potential Outliers:\n", outliers)

df = df[df["Close"] < 90]  # remove too-large values
df = df[df["Close"] > 50]   # remove too-small values (if needed)

# --- 5) Add Day-of-Week Column ---
df["DayOfWeek"] = df.index.day_name()

# --- 6) Calculate Daily % Change ---
df["Pct_Change"] = df["Close"].pct_change() * 100.0

# --- 7) Average Daily % Change by Weekday ---
avg_daily_change = df.groupby("DayOfWeek")["Pct_Change"].mean().sort_values()
print("Average Daily % Change by Day of Week (AED/PKR):")
print(avg_daily_change)

# --- 8) Plot: Bar Chart of Avg Daily % Change ---
avg_daily_change.plot(
    kind="bar",
    figsize=(8, 5),
    title="Average Daily % Change AED/PKR by Day of Week",
    ylabel="Average % Change",
    xlabel="Day of Week",
    color="skyblue"
)
plt.axhline(y=0, color="black", linewidth=1)
plt.tight_layout()
plt.show()

# --- 9) Plot: Historical AED/PKR Exchange Rate ---
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Close"], label="AED/PKR Close", color="blue")
plt.title("Historical AED/PKR Exchange Rate")
plt.xlabel("Date")
plt.ylabel("Exchange Rate (PKR per 1 AED)")
plt.legend()
plt.show()

# --- 10) Other Stats (Median, Std Dev) ---
median_daily_change = df.groupby("DayOfWeek")["Pct_Change"].median()
std_daily_change = df.groupby("DayOfWeek")["Pct_Change"].std()

print("Median Daily % Change by Day of Week (AED/PKR):")
print(median_daily_change)

print("\nStandard Deviation of Daily % Change by Day of Week (AED/PKR):")
print(std_daily_change)

# --- 11) Optionally Save to CSV for Replication ---
csv_filename = "aed_to_pkr_final_df.csv"
df.to_csv(csv_filename)
print(f"\nCleaned data saved to {csv_filename}")
