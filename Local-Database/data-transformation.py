import pandas as pd

# The downloaded data from TradingView needs to be transformed with this script
# The defaul ISO time format will not be accepted by DB, the time format needs to be adjusted

# Load CSV
df = pd.read_csv("data.csv")

# Convert timestamp format
df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d %H:%M:%S %z")

# Save back to CSV
df.to_csv("data_transformed.csv", index=False)