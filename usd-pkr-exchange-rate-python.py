import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# For plots to display inline in Jupyter notebooks
# %matplotlib inline  # Uncomment if using a Jupyter environment

# Download USD -> PKR (PKR=X) historical data
# Adjust start/end dates as you wish, e.g., from 2000-01-01 to today
df = yf.download("PKR=X", start="2010-01-01", end="2025-01-01", interval="1d")

# A quick peek at the data
print(df.head())
print(df.tail())

# Data Cleanup

# Drop any NaN rows
df.dropna(inplace=True)

# Check for outliers

outliers = df[df["Close"] > 400]
print(outliers)
#dropping outliers
df = df[df["Close"] < 400]
df = df[df["Close"] > 60]

# Create a column for day of week
# This returns Monday, Tuesday, etc.
df['DayOfWeek'] = df.index.day_name()

# Calculate the percentage change from the previous day's close
df['Pct_Change'] = df['Close'].pct_change() * 100.0  # in percentage

# Group by the weekday and compute average daily percentage change
avg_daily_change = df.groupby('DayOfWeek')['Pct_Change'].mean().sort_values()

print("Average Daily % Change by Day of Week:")
print(avg_daily_change)

avg_daily_change.plot(
    kind='bar',
    figsize=(8, 5),
    title='Average Daily % Change USD/PKR by Day of Week',
    ylabel='Average % Change',
    xlabel='Day of Week',
    color='skyblue'
)
plt.axhline(y=0, color='black', linewidth=1)
plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='USD/PKR Close', color='blue')
plt.title('Historical USD/PKR Exchange Rate')
plt.xlabel('Date')
plt.ylabel('Exchange Rate (PKR per USD)')
plt.legend()
plt.show()


# Average Daily % Change: If positive on a given weekday, on average the USD/PKR rate increased that day; if negative, the rate declined.

median_daily_change = df.groupby('DayOfWeek')['Pct_Change'].median()
std_daily_change = df.groupby('DayOfWeek')['Pct_Change'].std()
print("Median Daily % Change by Day of Week:")
print(median_daily_change)
print("\nStandard Deviation of Daily % Change by Day of Week:")
print(std_daily_change)


