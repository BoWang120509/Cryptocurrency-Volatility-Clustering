# Bash_Scan_Zip.py
# ----------------------------------------------
# Purpose: Simulate a bash command to list .parquet files in archive.zip
# Fulfilling the Bash command requirement of Data Processing stage
# ----------------------------------------------
import zipfile

zip_path = "archive.zip"

with zipfile.ZipFile(zip_path, 'r') as zipf:
    parquet_files = [f for f in zipf.namelist() if f.endswith('.parquet')]
    print(f"✅ .parquet file numbers: {len(parquet_files)}")

# Print first few files as preview (类似 bash ls | head)
print("\n📄 The first five files' names:")
for file in parquet_files[:5]:
    print(file)
