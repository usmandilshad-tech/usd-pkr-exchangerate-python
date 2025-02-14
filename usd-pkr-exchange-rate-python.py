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
