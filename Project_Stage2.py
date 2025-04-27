import zipfile
import pandas as pd
import numpy as np
import os
from io import BytesIO
from tqdm import tqdm

#-----------------------------------------
# Step 2. Get the features
#-----------------------------------------

ZIP_PATH = "archive.zip"
META_FILE = "coin_metadata_usdt.csv"# The output from stage 1
OUTPUT_FILE = "features_by_month.csv"# The output features


# ============ HELPER FUNCTIONS ============

def is_tidy(df):
    return df.index.name in ["open_time", "datetime"] and df.columns.is_unique

def compute_features(df, symbol, year, month):
    result = {"symbol": symbol, "month": f"{year}-{month:02d}"}
    
    df = df.copy()
    df = df[(df.index.year == year) & (df.index.month == month)]
    if len(df) < 100:
        return None

    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df.dropna(inplace=True)

    # Features
    result["log_return_std"] = df["log_return"].std() # To catch the strength of the volatility responde to the currency over the month
    result["volatility_15m"] = df["log_return"].rolling(15).std().mean() # The mean of the representative currency's high-frequency volatility over the month
    relative_range = (df["high"] - df["low"]) / df["close"]
    result["range_mean"] = relative_range.mean() # The relative average vibrate width, high minus low devided by the close price
    result["jump_freq"] = (np.abs(df["log_return"]) > 3 * result["log_return_std"]).mean() # The jumping behaviour of the currency, i.e. over the ratio of the extreme vol
    result["volume_std"] = np.log1p(df["volume"].std()) # The mean volatility of the trading volume of the representative currency over the month
    result["taker_buy_ratio_mean"] = (df["taker_buy_base_asset_volume"] / df["volume"]).replace([np.inf, -np.inf], np.nan).dropna().mean() # The volumn of the active buy-in over the total trading volumn
    result["number_of_trades"] = df["number_of_trades"].mean() # The number of trade in a minute, over a month
    result["return_skew"] = df["log_return"].skew() # This is the skewness, to determine the corresponding currency has sudden move or not during the month
    result["return_kurtosis"] = df["log_return"].kurt() # Kurtosis, if the corresponding currency's return has fat tail during the month, a complement feature for the jump frequency
    volume_rolling_mean = df["volume"].rolling(60).mean()
    result["volume_spike_ratio"] = (df["volume"] > 2 * volume_rolling_mean).mean() # The spike trading volumn during the month. To identify that some currencies might be news-driven type
    
    result["extreme_flag"] = int(
    abs(result["return_skew"]) > 1.5 and result["return_kurtosis"] > 100) # I added this part to mark the extreme
    return result

# ============ MAIN PIPELINE ============

meta = pd.read_csv(META_FILE)
all_features = []

with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
    for i, row in tqdm(meta.iterrows(), total=len(meta)):
        symbol = row["symbol"]
        filename = symbol + ".parquet"

        try:
            with archive.open(filename) as file:
                raw = BytesIO(file.read())
                df = pd.read_parquet(raw)

            if not is_tidy(df):
                df = df.reset_index()
                if "open_time" in df.columns:
                    df["open_time"] = pd.to_datetime(df["open_time"])
                    df.set_index("open_time", inplace=True)

            years = df.index.year.unique()
            for y in years:
                for m in range(1, 13):
                    f = compute_features(df, symbol, y, m)
                    if f:
                        all_features.append(f)

        except Exception as e:
            print(f"Skip {symbol}: {e}")

features_df = pd.DataFrame(all_features)
features_df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved to {OUTPUT_FILE}")

# Based on my observation
# 1. The range_mean feature is diversified between different currencies in different ranges. Some may reach to 1, some under 0.0005.
# I suggest using relative range, (high-low)/close, to replace the range mean. Changed above
# 2. The volume standard deviation has a significant difference, some may reach to 500000. That is reasonable.
# But I can standarize them by using volumn_std/mean(volume) or StandardScaler() before doing the clustering. I changed above.
# 3. The skewness and kurtosis have some interesting observations. When the absolute value of the skewness is high (>100 for example), the kurtosis could be over 10000.
# Skewness measures whether the currency at a specific period "tails" to one side
# Kurtosis measures the thickness of the tail, whether extreme values ​​appear frequently and in a concentrated manner
# Therefore, I think that when a currency has a very biased one-sided surge or plunge in a certain period of time, and it occurs multiple times in a concentrated manner, this may lead to this situation.
# For example, SUN occurs a extremely abnormal situation during June, 2021. Its skewness below -190 and the kurtosis above 35000. 
# This could be a typical "high vol, high jumps, bearish" behavior. The log return goes to the left tail, which could be a common case for fake-orders/manupilating.
