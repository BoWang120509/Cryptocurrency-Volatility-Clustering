import zipfile
import pandas as pd
from io import BytesIO

#-----------------------------------------
# Step 1. Loading Data and knocking out the abnormal currencies (leveraged or contract) to get only the USDT-based crptocurrencies for the next step
#-----------------------------------------
def scan_zip_parquet_metadata(zip_path, max_files=None):
    records = []

    with zipfile.ZipFile(zip_path, 'r') as z:
        parquet_files = [f for f in z.namelist() if f.endswith('.parquet')]
        if max_files:
            parquet_files = parquet_files[:max_files]

        for file in parquet_files:
            try:
                with z.open(file) as f:
                    df = pd.read_parquet(BytesIO(f.read()), engine='pyarrow', columns=["open_time"])
                    df.index = pd.to_datetime(df.index)

                    symbol = file.replace("_1m.parquet", "").split('/')[-1]
                    start = df.index.min()
                    end = df.index.max()
                    rows = len(df)
                    duration = (end - start).days

                    records.append({
                        "symbol": symbol,
                        "start_time": start,
                        "end_time": end,
                        "row_count": rows,
                        "duration_days": duration
                    })
            except Exception as e:
                print(f"Failed: {file} | Error: {e}")
                continue

    return pd.DataFrame(records)

zip_path = "archive.zip"
meta_df = scan_zip_parquet_metadata(zip_path)

meta_df.to_csv("coin_metadata.csv", index=False)
print("Saved to coin_metadata.csv")

meta = pd.read_csv("coin_metadata.csv")
meta['symbol'] = meta['symbol'].str.replace('.parquet', '', regex=False)
meta['symbol'] = meta['symbol'].str.upper()

# Filtering the USDT-based currencies
meta_usdt = meta[meta['symbol'].str.endswith('USDT')].copy()

# Exclude the abnormal currencies
meta_usdt = meta_usdt[~meta_usdt['symbol'].str.contains(r'\d|UP|DOWN|BULL|BEAR|3L|3S', case=False)]

print("The original pairs：", len(meta))
print("The USDT-based pairs：", len(meta_usdt))

meta_usdt.to_csv("coin_metadata_usdt.csv", index=False)

